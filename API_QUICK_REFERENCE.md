# TrueNAS API Quick Reference

## Connection

```python
# WebSocket URL
wss://<host>/api/current

# Authentication
{
    "method": "auth.login_with_api_key",
    "jsonrpc": "2.0",
    "id": 0,
    "params": ["<api-key>"]
}
```

## System Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `system.info` | System information | None | version, hostname, physmem, uptime_seconds |
| `system.ready` | System ready status | None | Boolean |
| `update.check_available` | Check updates | None | status, version, changelog |

## Storage Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `pool.query` | List pools | filters (opt) | id, name, status, healthy, topology |
| `pool.dataset.query` | List datasets | filters (opt) | id, pool, type, used, available, quota |
| `disk.query` | List disks | filters (opt) | name, serial, size, type, model, pool |
| `disk.temperature_alerts` | Disk temps | None | {disk_id: temp_data} |
| `boot.get_state` | Boot pool state | None | id, properties, status |

## Network Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `interface.query` | List interfaces | filters (opt) | id, name, type, state, mtu |

## Service Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `service.query` | List services | filters (opt) | id, service, enable, state, pids |

## Virtualization Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `virt.instance.query` | List VMs | filters (opt) | id, name, status, vcpus, memory |
| `app.query` | List apps | filters (opt) | id, name, state, version, update_available |

## Task Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `cloudsync.query` | Cloud sync tasks | filters (opt) | id, direction, path, enabled, job |
| `replication.query` | Replication tasks | filters (opt) | id, name, source_datasets, enabled |
| `pool.snapshottask.query` | Snapshot tasks | filters (opt) | id, dataset, recursive, schedule |

## Monitoring Methods

| Method | Description | Parameters | Key Fields |
|--------|-------------|------------|------------|
| `reporting.netdata_get_data` | Performance data | graph specs | Metrics by graph type |
| `core.get_jobs` | Job status | filters (opt) | id, method, progress, state |

## Common Graph Types

For `reporting.netdata_get_data`:

```python
[
    {"name": "cpu"},              # CPU usage
    {"name": "cputemp"},          # CPU temperature
    {"name": "memory"},           # Memory usage
    {"name": "interface",         # Network stats
     "identifier": "eth0"},
    {"name": "disk"},             # Disk I/O
    {"name": "load"}              # System load
]
```

## Query Filter Examples

### Basic Filter
```python
[["field", "=", "value"]]
```

### Multiple Conditions
```python
[
    ["type", "=", "HDD"],
    ["size", ">", 1000000000000]
]
```

### Complex Filter
```python
[
    ["status", "=", "ONLINE"],
    "OR",
    ["status", "=", "DEGRADED"]
]
```

## Common Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals | `["name", "=", "tank"]` |
| `!=` | Not equals | `["state", "!=", "STOPPED"]` |
| `>` | Greater than | `["size", ">", 100]` |
| `<` | Less than | `["used", "<", 50]` |
| `>=` | Greater or equal | `["temp", ">=", 70]` |
| `<=` | Less or equal | `["load", "<=", 1.0]` |
| `~` | Regex match | `["name", "~", "^tank"]` |
| `in` | In list | `["type", "in", ["SSD", "NVMe"]]` |
| `nin` | Not in list | `["state", "nin", ["OFFLINE"]]` |

## Response Formats

### Success Response
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": { /* data */ }
}
```

### Error Response
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "error": {
        "message": "Error message",
        "code": "ERROR_CODE",
        "data": {
            "reason": "Detailed reason"
        }
    }
}
```

## Example API Calls

### Get System Info
```json
{
    "method": "system.info",
    "jsonrpc": "2.0",
    "id": 0,
    "params": []
}
```

### Query Pools
```json
{
    "method": "pool.query",
    "jsonrpc": "2.0",
    "id": 0,
    "params": []
}
```

### Query Specific Pool
```json
{
    "method": "pool.query",
    "jsonrpc": "2.0",
    "id": 0,
    "params": [[["name", "=", "tank"]]]
}
```

### Get Disk Temperatures
```json
{
    "method": "disk.temperature_alerts",
    "jsonrpc": "2.0",
    "id": 0,
    "params": []
}
```

### Get CPU Metrics
```json
{
    "method": "reporting.netdata_get_data",
    "jsonrpc": "2.0",
    "id": 0,
    "params": [[{"name": "cpu"}]]
}
```

### Check Job Status
```json
{
    "method": "core.get_jobs",
    "jsonrpc": "2.0",
    "id": 0,
    "params": [[["id", "=", 123]]]
}
```

## Python Example

```python
import websockets
import json
import asyncio

async def query_truenas(host, api_key, method, params=None):
    url = f"wss://{host}/api/current"
    
    async with websockets.connect(url, ssl=ssl_context) as ws:
        # Authenticate
        auth = {
            "method": "auth.login_with_api_key",
            "jsonrpc": "2.0",
            "id": 0,
            "params": [api_key]
        }
        await ws.send(json.dumps(auth))
        response = await ws.recv()
        auth_result = json.loads(response)
        
        if not auth_result.get("result"):
            raise Exception("Authentication failed")
        
        # Query
        query = {
            "method": method,
            "jsonrpc": "2.0",
            "id": 1,
            "params": params or []
        }
        await ws.send(json.dumps(query))
        response = await ws.recv()
        result = json.loads(response)
        
        return result.get("result")

# Usage
data = await query_truenas(
    "192.168.1.100",
    "your-api-key",
    "system.info"
)
```

## Common Error Codes

| Code | Description | Common Cause |
|------|-------------|--------------|
| `EACCES` | Permission denied | Insufficient API key permissions |
| `ENOENT` | Not found | Resource doesn't exist |
| `EINVAL` | Invalid argument | Invalid parameters |
| `EEXIST` | Already exists | Duplicate resource |
| `EBUSY` | Resource busy | Operation in progress |

## Rate Limiting

- No explicit rate limits documented
- Recommended: 1 request per second for continuous polling
- Integration uses 60-second intervals for most sensors

## Best Practices

1. **Reuse WebSocket Connection**: Keep connection open for multiple queries
2. **Handle Reconnection**: Implement automatic reconnection logic
3. **Cache Results**: Cache data when appropriate to reduce API calls
4. **Use Filters**: Filter data at API level rather than client side
5. **Error Handling**: Always check for error responses
6. **Logging**: Log API calls for debugging (without sensitive data)

## Security Notes

- **API Keys**: Never log or expose API keys
- **SSL/TLS**: Use valid certificates in production
- **Permissions**: Use least-privilege API keys when possible
- **Rotation**: Rotate API keys regularly

## Resources

- **API Docs**: `https://<your-truenas>/api/docs/`
- **Forums**: https://www.truenas.com/community/
- **Documentation**: https://www.truenas.com/docs/
- **Source Code**: https://github.com/truenas/middleware

---

*Quick Reference for TrueNAS SCALE v25.10.2 API*
