# TrueNAS Home Assistant Integration (Updated for v25.10.2 API)

This is an updated version of the TrueNAS integration for Home Assistant, compatible with **TrueNAS SCALE v25.10.2** API specifications.

## Overview

This custom integration allows Home Assistant to monitor and interact with TrueNAS SCALE systems. It provides sensors for system information, disks, pools, datasets, virtual machines, apps, and more.

## What's New in This Version

This version has been updated to align with the TrueNAS SCALE v25.10.2 API specifications while maintaining full backward compatibility with existing functionality.

### API Changes from Previous Versions

The integration now explicitly documents and supports the v25.10.2 API structure:

1. **WebSocket API Endpoint**: `wss://<host>/api/current`
2. **Authentication Method**: `auth.login_with_api_key`
3. **JSON-RPC 2.0 Protocol**: All API calls use standard JSON-RPC 2.0 format

### Supported API Methods

The integration uses the following TrueNAS v25.10.2 API methods:

#### System Information
- `system.info` - Get basic system information (version, hostname, memory, etc.)
- `system.ready` - Check if system is ready
- `update.check_available` - Check for available system updates

#### Storage
- `pool.query` - Query storage pools
- `pool.dataset.query` - Query datasets within pools
- `disk.query` - Query physical disks
- `disk.temperature_alerts` - Get disk temperature data
- `boot.get_state` - Get boot pool state

#### Network
- `interface.query` - Query network interfaces

#### Services & Applications
- `service.query` - Query system services status
- `app.query` - Query installed applications (Docker containers)
- `virt.instance.query` - Query virtual machines

#### Tasks & Jobs
- `cloudsync.query` - Query cloud synchronization tasks
- `replication.query` - Query replication tasks
- `pool.snapshottask.query` - Query snapshot tasks
- `core.get_jobs` - Get job status and progress

#### Monitoring
- `reporting.netdata_get_data` - Get performance metrics and statistics

## Features

### System Monitoring
- System version and uptime
- CPU usage, load averages, and temperature
- Memory usage (total, used, free, cached, ARC cache)
- Update availability and installation progress

### Storage Monitoring
- Pool status, capacity, and health
- Dataset information and quotas
- Disk status and SMART data
- Boot pool status

### Network Monitoring
- Interface status and statistics
- Link state and speed
- RX/TX data transfer

### Service Monitoring
- Service status (running/stopped)
- Service state monitoring

### Virtualization & Apps
- Virtual machine status
- Application (container) status
- Container statistics

### Tasks Monitoring
- Cloud sync task status
- Replication task status
- Snapshot task status

## Installation

### HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the upper right corner
4. Select "Custom repositories"
5. Add this repository URL
6. Select "Integration" as the category
7. Click "Add"
8. Find "TrueNAS" in the list and install

### Manual Installation
1. Copy the `custom_components/truenas` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

### Generating an API Key

1. Log in to your TrueNAS SCALE web interface
2. Go to **System Settings** > **API Keys**
3. Click **Add** to create a new API key
4. Give it a name (e.g., "Home Assistant")
5. Click **Add** and copy the generated key
6. **Important**: Save this key securely - it will only be shown once!

### Adding the Integration

1. In Home Assistant, go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for "TrueNAS"
4. Enter your TrueNAS details:
   - **Host**: IP address or hostname of your TrueNAS system
   - **API Key**: The API key you generated
   - **Verify SSL**: Enable if using valid SSL certificate
5. Click **Submit**

## API Documentation

For complete API documentation, refer to the official TrueNAS API documentation:
- **API Methods**: Available at `https://<your-truenas-ip>/api/docs/` (requires authentication)
- **WebSocket API**: `wss://<your-truenas-ip>/api/current`

### API Call Format

All API calls use JSON-RPC 2.0 format:

```json
{
    "method": "system.info",
    "jsonrpc": "2.0",
    "id": 0,
    "params": []
}
```

Response format:
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": {
        "version": "TrueNAS-SCALE-25.10.2",
        "hostname": "truenas",
        "physmem": 34359738368,
        ...
    }
}
```

## Sensors

### System Sensors
- System Version
- Hostname
- Uptime
- CPU Usage
- CPU Temperature (if available)
- Load Average (1m, 5m, 15m)
- Memory Usage
- ARC Cache Size
- Update Available
- Update Version

### Storage Sensors
- Pool Status
- Pool Capacity (used/available)
- Pool Health
- Dataset Information
- Disk Status
- Disk Temperature

### Network Sensors
- Interface Link State
- Interface Speed
- RX/TX Bytes
- RX/TX Packets

### Service Sensors
- Service Status (for each monitored service)
- Service State

### VM & App Sensors
- VM Status
- VM State
- App Status
- App State

### Task Sensors
- Cloud Sync Task State
- Replication Task State
- Snapshot Task State

## Binary Sensors

- Pool Health (healthy/unhealthy)
- Service Running Status
- Update Available
- VM Running Status
- App Running Status

## Update Entity

The integration provides an update entity that shows:
- Current TrueNAS version
- Available update version
- Installation progress
- Ability to trigger updates (if supported)

## Services

The integration may expose services for controlling TrueNAS (check `services.yaml` for available services).

## Troubleshooting

### Connection Issues

1. **Certificate Verification Failed**
   - Either install a valid SSL certificate on TrueNAS
   - Or disable SSL verification in the integration configuration

2. **WebSocket Not Supported**
   - Ensure you're connecting to the correct port (typically 443 for HTTPS)
   - Verify TrueNAS is running version compatible with WebSocket API

3. **Authentication Failed**
   - Verify the API key is correct and has not been revoked
   - Regenerate the API key if necessary

4. **API Not Found (404)**
   - Ensure you're running TrueNAS SCALE (not CORE)
   - Verify the API endpoint is `/api/current`

### Debug Logging

To enable debug logging, add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.truenas: debug
```

## Compatibility

- **TrueNAS SCALE**: v22.02 and later (tested with v25.10.2)
- **Home Assistant**: 2023.1 or later
- **Python**: 3.11 or later

## API Method Reference

### Quick Reference Table

| Method | Purpose | Returns |
|--------|---------|---------|
| `system.info` | System information | Object with version, hostname, memory, etc. |
| `interface.query` | Network interfaces | Array of interface objects |
| `disk.query` | Disk information | Array of disk objects |
| `pool.query` | Storage pools | Array of pool objects |
| `pool.dataset.query` | Datasets | Array of dataset objects |
| `virt.instance.query` | Virtual machines | Array of VM objects |
| `app.query` | Applications | Array of app objects |
| `service.query` | Services | Array of service objects |
| `cloudsync.query` | Cloud sync tasks | Array of task objects |
| `replication.query` | Replication tasks | Array of task objects |
| `pool.snapshottask.query` | Snapshot tasks | Array of task objects |
| `update.check_available` | Update check | Object with update info |
| `core.get_jobs` | Job status | Array of job objects |
| `reporting.netdata_get_data` | Performance data | Metrics object |

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project maintains the same license as the original TrueNAS integration.

## Credits

Original integration by [@tomaae](https://github.com/tomaae)
Updated for TrueNAS v25.10.2 API compatibility

## Support

For issues and feature requests:
- GitHub Issues: [Create an issue](https://github.com/tomaae/homeassistant-truenas/issues)

For TrueNAS API documentation:
- Visit `https://<your-truenas-ip>/api/docs/`
- Official TrueNAS Documentation: https://www.truenas.com/docs/

## Changelog

### Version 2.0.0
- Updated for TrueNAS SCALE v25.10.2 API specifications
- Enhanced API documentation
- Maintained backward compatibility with existing functionality
- Added comprehensive API method documentation
- Improved error handling and logging
- Updated connection handling for WebSocket API

### Previous Versions
See original repository for historical changelog.
