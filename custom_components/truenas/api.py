"""TrueNAS API - Updated for TrueNAS v25.10.2 API Specifications.

This module provides a WebSocket-based API client for TrueNAS SCALE v25.10.2.
The API uses JSON-RPC 2.0 over WebSocket connections.

API Documentation: https://www.truenas.com/docs/api/
"""

from logging import getLogger
from threading import Lock
from typing import Any

import ssl
import json
from websockets.sync.client import connect, ClientConnection

_LOGGER = getLogger(__name__)


# ---------------------------
#   TrueNASAPI
# ---------------------------
class TrueNASAPI(object):
    """Handle all communication with TrueNAS using the v25.10.2 API specification.
    
    This client connects to TrueNAS SCALE v25.10.2 via WebSocket and uses JSON-RPC 2.0
    for method calls. The API endpoint is: wss://<host>/api/current
    
    Key API Methods (as per v25.10.2 documentation):
    - system.info: Returns basic system information
    - interface.query: Query network interfaces
    - disk.query: Query disk information
    - pool.query: Query storage pools
    - pool.dataset.query: Query datasets
    - virt.instance.query: Query virtual machines (VMs)
    - app.query: Query installed applications
    - service.query: Query system services
    - cloudsync.query: Query cloud sync tasks
    - replication.query: Query replication tasks
    - pool.snapshottask.query: Query snapshot tasks
    - update.check_available: Check for system updates
    - core.get_jobs: Get job status
    - reporting.netdata_get_data: Get performance metrics
    - disk.temperature_alerts: Get disk temperature data
    - boot.get_state: Get boot pool state
    """

    _ws: ClientConnection

    def __init__(
        self,
        host: str,
        api_key: str,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize the TrueNAS API client.
        
        Args:
            host: TrueNAS hostname or IP address
            api_key: API key for authentication (generated in TrueNAS UI)
            verify_ssl: Whether to verify SSL certificates
        """
        self._host = host
        self._api_key = api_key
        self._ssl_verify = verify_ssl
        self._url = f"wss://{self._host}/api/current"
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self._ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        if verify_ssl:
            self._ssl_context.check_hostname = True
            self._ssl_context.verify_mode = ssl.CERT_REQUIRED
        else:
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE

        self.lock = Lock()
        self._connected = False
        self._error = ""
        self._error_logged = False

    # ---------------------------
    #   connect
    # ---------------------------
    def connect(self) -> bool:
        """Establish WebSocket connection and authenticate.
        
        Connection process:
        1. Open WebSocket connection to wss://<host>/api/current
        2. Authenticate using auth.login_with_api_key method
        3. Receive authentication response
        
        Returns:
            bool: True if connected and authenticated successfully
        """
        with self.lock:
            self._connected = False
            self._error = ""
            try:
                # Disable SNI when verify_ssl is False to avoid TLSV1_UNRECOGNIZED_NAME errors
                connection_kwargs = {
                    "ssl": self._ssl_context,
                    "max_size": 16777216,
                    "ping_interval": 20,
                }
                if not self._ssl_verify:
                    connection_kwargs["server_hostname"] = ""

                self._ws = connect(self._url, **connection_kwargs)
            except Exception as e:
                if "CERTIFICATE_VERIFY_FAILED" in str(e.args):
                    self._error = "certificate_verify_failed"

                if "The plain HTTP request was sent to HTTPS port" in str(e.args):
                    self._error = "http_used"

                if "TLSV1_UNRECOGNIZED_NAME" in str(e.args):
                    self._error = "tlsv1_not_supported"

                if "No WebSocket UPGRADE" in str(e.args):
                    self._error = "websocket_not_supported"

                if "No address associated with hostname" in e.args:
                    self._error = "unknown_hostname"

                if "Connection refused" in e.args:
                    self._error = "connection_refused"

                if "No route to host" in e.args or "Name or service not known" in str(
                    e
                ):
                    self._error = "invalid_hostname"

                if "timed out while waiting for handshake response" in e.args:
                    self._error = "handshake_timeout"

                if "404" in str(e):
                    self._error = "api_not_found"

                if not self._error_logged:
                    _LOGGER.error("TrueNAS %s failed to connect (%s)", self._host, e)

                self._error_logged = True
                return False

            try:
                # Authenticate using auth.login_with_api_key (v25.10.2 API)
                payload = {
                    "method": "auth.login_with_api_key",
                    "jsonrpc": "2.0",
                    "id": 0,
                    "params": [self._api_key],
                }
                self._ws.send(json.dumps(payload))
                message = self._ws.recv()
                data = json.loads(message)
                self._connected = data["result"]
                if not self._connected:
                    self._error = "invalid_key"

            except Exception as e:
                if not self._error_logged:
                    _LOGGER.error("TrueNAS %s failed to login (%s)", self._host, e)

                self._error_logged = True
                return False

            self._error_logged = False
            return self._connected

    # ---------------------------
    #   disconnect
    # ---------------------------
    def disconnect(self) -> bool:
        """Close WebSocket connection.
        
        Returns:
            bool: Always returns False (disconnected state)
        """
        if hasattr(self, "_ws") and self._ws:
            self._ws.close()

        self._connected = False
        return self._connected

    # ---------------------------
    #   reconnect
    # ---------------------------
    def reconnect(self) -> bool:
        """Disconnect and reconnect to TrueNAS.
        
        Returns:
            bool: Connection state after reconnection attempt
        """
        self.disconnect()
        self.connect()
        return self._connected

    # ---------------------------
    #   connected
    # ---------------------------
    def connected(self) -> bool:
        """Check if currently connected to TrueNAS.
        
        Returns:
            bool: Current connection state
        """
        return self._connected

    # ---------------------------
    #   connection_test
    # ---------------------------
    def connection_test(self) -> tuple:
        """Test the connection by connecting and querying system.info.
        
        Returns:
            tuple: (connected: bool, error: str)
        """
        self.connect()
        if self.connected():
            self.query("system.info")

        return self._connected, self._error

    # ---------------------------
    #   query
    # ---------------------------
    def query(self, service: str, params: dict[str, Any] | None = {}) -> list | None:
        """Execute an API query using JSON-RPC 2.0.
        
        This method sends a JSON-RPC 2.0 request to the TrueNAS API. The request format is:
        {
            "method": "<service>",
            "jsonrpc": "2.0",
            "id": 0,
            "params": [<params>]
        }
        
        Common TrueNAS v25.10.2 API methods:
        - system.info: Get system information
        - interface.query: Get network interfaces
        - disk.query: Get disks
        - pool.query: Get storage pools
        - pool.dataset.query: Get datasets
        - virt.instance.query: Get virtual machines
        - app.query: Get applications
        - service.query: Get services
        - cloudsync.query: Get cloud sync tasks
        - replication.query: Get replication tasks
        - pool.snapshottask.query: Get snapshot tasks
        - update.check_available: Check for updates
        - reporting.netdata_get_data: Get metrics
        
        Args:
            service: The API method name (e.g., "system.info")
            params: Parameters for the method (optional)
        
        Returns:
            The result data from the API, or None if query failed
        """
        if not self.connected():
            self.connect()

        with self.lock:
            self._error = ""
            try:
                _LOGGER.debug(
                    "TrueNAS %s query: %s, %s",
                    self._host,
                    service,
                    params,
                )
                payload = {
                    "method": service,
                    "jsonrpc": "2.0",
                    "id": 0,
                    "params": [],
                }
                if params != {}:
                    if type(params) is not list:
                        params = [params]
                    payload["params"] = params

                self._ws.send(json.dumps(payload))
                message = self._ws.recv()
                if message.startswith("{"):
                    data = json.loads(message)
                    if "result" in data:
                        data = data["result"]
                    else:
                        self._error = "malformed_result"

                    if (type(data) is list or type(data) is dict) and "error" in data:
                        if (
                            "data" in data["error"]
                            and "reason" in data["error"]["data"]
                        ):
                            _LOGGER.error(
                                "TrueNAS %s query (%s) error: %s",
                                self._host,
                                service,
                                data["error"]["data"]["reason"],
                            )
                        else:
                            _LOGGER.error(
                                "TrueNAS %s query (%s) error: %s",
                                self._host,
                                service,
                                data["error"]["message"],
                            )
                else:
                    data = message

                _LOGGER.debug(
                    "TrueNAS %s query (%s) response: %s", self._host, service, data
                )
            except Exception as e:
                _LOGGER.warning(
                    'TrueNAS %s unable to fetch data "%s" (%s)',
                    self._host,
                    service,
                    e,
                )
                self.disconnect()
                self._error = str(e)
                return None

            return data

    @property
    def error(self):
        """Get the last error message.
        
        Returns:
            str: Last error message or empty string
        """
        return self._error
