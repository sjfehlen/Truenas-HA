# TrueNAS API Migration Guide - v25.10.2

This document outlines the API changes and improvements in TrueNAS SCALE v25.10.2 and how they affect the Home Assistant integration.

## Overview

The TrueNAS SCALE v25.10.2 API maintains backward compatibility with previous versions while introducing some refinements and additional capabilities. The integration has been updated to explicitly document and support the latest API structure.

## Connection & Authentication

### WebSocket Connection
**Endpoint**: `wss://<host>/api/current`

The WebSocket API endpoint remains the same, providing a persistent connection for API calls using JSON-RPC 2.0 protocol.

### Authentication Method
**Method**: `auth.login_with_api_key`

**Request Format**:
```json
{
    "method": "auth.login_with_api_key",
    "jsonrpc": "2.0",
    "id": 0,
    "params": ["<your-api-key>"]
}
```

**Response Format**:
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "result": true
}
```

## Core API Methods

### 1. System Information

#### system.info
Returns comprehensive system information.

**Method**: `system.info`
**Parameters**: None

**Response Fields (v25.10.2)**:
- `version`: TrueNAS version string
- `buildtime`: Build timestamp (ISO 8601 format)
- `hostname`: System hostname
- `physmem`: Physical memory in bytes
- `model`: System model
- `cores`: Number of CPU cores
- `physical_cores`: Number of physical CPU cores
- `loadavg`: Array of load averages [1m, 5m, 15m]
- `uptime`: System uptime string
- `uptime_seconds`: Uptime in seconds
- `system_serial`: System serial number
- `system_product`: System product name
- `system_manufacturer`: System manufacturer
- `license`: License information
- `ecc_memory`: ECC memory status
- `system_product_version`: Product version
- `timezone`: System timezone
- `datetime`: Current system datetime

**Example Response**:
```json
{
    "version": "TrueNAS-SCALE-25.10.2",
    "buildtime": "2025-01-15T10:30:00+00:00",
    "hostname": "truenas",
    "physmem": 34359738368,
    "cores": 8,
    "uptime_seconds": 86400,
    "system_manufacturer": "Supermicro",
    ...
}
```

### 2. Storage Management

#### pool.query
Query storage pools.

**Method**: `pool.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Pool ID
- `name`: Pool name
- `guid`: Pool GUID
- `status`: Pool status (ONLINE, DEGRADED, etc.)
- `path`: Pool mount path
- `scan`: Scrub/resilver information
- `healthy`: Boolean health status
- `is_decrypted`: Encryption status
- `topology`: Pool topology (vdevs, cache, log, etc.)

#### pool.dataset.query
Query datasets within pools.

**Method**: `pool.dataset.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Dataset ID/path
- `name`: Dataset name
- `pool`: Parent pool
- `type`: Dataset type (FILESYSTEM, VOLUME)
- `mountpoint`: Mount point
- `used`: Space used (object with raw_value, parsed)
- `available`: Space available (object with raw_value, parsed)
- `quota`: Quota settings
- `compression`: Compression algorithm
- `deduplication`: Dedup status
- `readonly`: Read-only status
- `encryption`: Encryption status

### 3. Disk Management

#### disk.query
Query physical disks.

**Method**: `disk.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `identifier`: Disk identifier
- `name`: Disk device name (e.g., "sda")
- `subsystem`: Subsystem type
- `number`: Disk number
- `serial`: Serial number
- `size`: Disk size in bytes
- `type`: Disk type (HDD, SSD)
- `model`: Disk model
- `rotationrate`: Rotation rate (for HDDs)
- `bus`: Bus type (SATA, SAS, etc.)
- `devname`: Device name
- `enclosure`: Enclosure information (if applicable)
- `pool`: Pool this disk belongs to (if any)

#### disk.temperature_alerts
Get disk temperature information.

**Method**: `disk.temperature_alerts`
**Parameters**: None

**Response**: Dictionary mapping disk identifiers to temperature data

### 4. Network Management

#### interface.query
Query network interfaces.

**Method**: `interface.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Interface ID
- `name`: Interface name (e.g., "eth0")
- `description`: Interface description
- `type`: Interface type (PHYSICAL, VLAN, BOND, BRIDGE)
- `state`: Interface state object containing:
  - `name`: State name
  - `link_state`: Link state (LINK_STATE_UP, LINK_STATE_DOWN)
  - `active_media_type`: Active media type
  - `active_media_subtype`: Active media subtype
  - `link_address`: MAC address
  - `aliases`: IP aliases
- `mtu`: Maximum transmission unit
- `enabled`: Interface enabled status

### 5. Virtualization

#### virt.instance.query
Query virtual machine instances.

**Method**: `virt.instance.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: VM ID
- `name`: VM name
- `description`: VM description
- `type`: VM type
- `status`: VM status (RUNNING, STOPPED, etc.)
- `cpu_mode`: CPU mode
- `cpu_model`: CPU model
- `vcpus`: Number of virtual CPUs
- `memory`: Memory allocated in MB
- `bootloader`: Bootloader type
- `devices`: Array of attached devices
- `autostart`: Autostart on boot

### 6. Applications

#### app.query
Query installed applications (Docker containers).

**Method**: `app.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: App ID
- `name`: App name
- `state`: Application state (RUNNING, STOPPED, etc.)
- `version`: App version
- `human_version`: Human-readable version
- `latest_version`: Latest available version
- `update_available`: Boolean update status
- `metadata`: App metadata
- `config`: App configuration
- `resources`: Resource allocation

### 7. Services

#### service.query
Query system services.

**Method**: `service.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Service ID
- `service`: Service name
- `enable`: Service enabled status
- `state`: Service state (RUNNING, STOPPED)
- `pids`: Process IDs

### 8. Tasks

#### cloudsync.query
Query cloud synchronization tasks.

**Method**: `cloudsync.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Task ID
- `description`: Task description
- `direction`: Sync direction (PUSH, PULL)
- `transfer_mode`: Transfer mode (SYNC, COPY, MOVE)
- `path`: Local path
- `credentials`: Credential ID
- `attributes`: Sync attributes
- `enabled`: Task enabled status
- `job`: Current job information (if running)

#### replication.query
Query replication tasks.

**Method**: `replication.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Task ID
- `name`: Task name
- `source_datasets`: Source dataset list
- `target_dataset`: Target dataset
- `recursive`: Recursive replication
- `enabled`: Task enabled status
- `direction`: Replication direction
- `transport`: Transport method
- `retention_policy`: Snapshot retention policy
- `job`: Current job information (if running)

#### pool.snapshottask.query
Query snapshot tasks.

**Method**: `pool.snapshottask.query`
**Parameters**: Optional query filters

**Key Response Fields**:
- `id`: Task ID
- `dataset`: Dataset to snapshot
- `recursive`: Recursive snapshot
- `lifetime_value`: Snapshot retention value
- `lifetime_unit`: Snapshot retention unit
- `naming_schema`: Snapshot naming pattern
- `schedule`: Cron schedule
- `enabled`: Task enabled status

### 9. Updates

#### update.check_available
Check for available system updates.

**Method**: `update.check_available`
**Parameters**: None

**Response Fields**:
- `status`: Update status (AVAILABLE, NO_UPDATE, etc.)
- `version`: Available version
- `changelog`: Update changelog
- `notes`: Update notes

### 10. Monitoring

#### reporting.netdata_get_data
Get performance metrics from Netdata.

**Method**: `reporting.netdata_get_data`
**Parameters**: 
- Array of graph specifications:
  - `name`: Graph name
  - `identifier`: Resource identifier (optional)

**Common Graphs**:
- `cpu`: CPU usage
- `cputemp`: CPU temperature (if available)
- `memory`: Memory usage
- `interface`: Network interface statistics
- `disk`: Disk I/O
- `load`: System load

**Example Request**:
```json
{
    "method": "reporting.netdata_get_data",
    "jsonrpc": "2.0",
    "id": 0,
    "params": [[
        {"name": "cpu"},
        {"name": "memory"}
    ]]
}
```

### 11. Job Management

#### core.get_jobs
Get information about running or completed jobs.

**Method**: `core.get_jobs`
**Parameters**: 
- Query filters (optional)

**Response**: Array of job objects

**Job Fields**:
- `id`: Job ID
- `method`: API method the job is executing
- `arguments`: Job arguments
- `progress`: Progress object containing:
  - `percent`: Percentage complete
  - `description`: Progress description
- `state`: Job state (RUNNING, SUCCESS, FAILED, etc.)
- `result`: Job result (when complete)
- `error`: Error message (if failed)
- `exception`: Exception details (if failed)
- `time_started`: Start timestamp
- `time_finished`: Finish timestamp

## Query Filters

Many API methods support query filters for filtering, sorting, and limiting results.

### Filter Format
```python
[
    ["field", "operator", "value"],
    ["field2", "operator2", "value2"],
    ...
]
```

### Common Operators
- `=`: Equals
- `!=`: Not equals
- `>`: Greater than
- `<`: Less than
- `>=`: Greater than or equal
- `<=`: Less than or equal
- `~`: Regex match
- `in`: Value in list
- `nin`: Value not in list

### Example with Filters
```json
{
    "method": "disk.query",
    "jsonrpc": "2.0",
    "id": 0,
    "params": [[
        ["type", "=", "HDD"],
        ["size", ">", 1000000000000]
    ]]
}
```

## Error Handling

### Error Response Format
```json
{
    "id": 0,
    "jsonrpc": "2.0",
    "error": {
        "message": "Error message",
        "code": error_code,
        "data": {
            "reason": "Detailed reason"
        }
    }
}
```

### Common Error Codes
- `EACCES`: Permission denied
- `ENOENT`: Not found
- `EINVAL`: Invalid argument
- `EEXIST`: Already exists

## Best Practices

### 1. Connection Management
- Maintain a persistent WebSocket connection
- Implement automatic reconnection on disconnection
- Use connection pooling for concurrent requests

### 2. Error Handling
- Always check for errors in API responses
- Implement retry logic for transient errors
- Log errors for debugging

### 3. Performance
- Use query filters to limit data returned
- Cache frequently accessed data
- Batch related queries when possible
- Use appropriate polling intervals (60 seconds recommended for most sensors)

### 4. Authentication
- Store API keys securely
- Never log API keys
- Regenerate API keys periodically
- Use dedicated API keys per integration

## Migration Checklist

✅ WebSocket connection to `/api/current`
✅ JSON-RPC 2.0 format for all requests
✅ Authentication via `auth.login_with_api_key`
✅ Updated field names in responses
✅ Error handling for new error formats
✅ Query filter syntax
✅ Job status monitoring
✅ Metrics collection via `reporting.netdata_get_data`

## Version Compatibility

This integration is designed to work with:
- **TrueNAS SCALE 22.02+** (older versions)
- **TrueNAS SCALE 25.10.2** (latest, fully tested)
- **Future versions** (should maintain compatibility)

The API methods used by this integration are stable and should continue to work in future TrueNAS releases.

## Additional Resources

- **Official API Documentation**: `https://<your-truenas-ip>/api/docs/`
- **TrueNAS Forums**: https://www.truenas.com/community/
- **TrueNAS Documentation**: https://www.truenas.com/docs/
- **GitHub Repository**: https://github.com/tomaae/homeassistant-truenas

## Support

For integration-specific issues:
- Check the README.md for troubleshooting steps
- Review debug logs with verbose logging enabled
- Submit issues on GitHub with relevant logs

For TrueNAS API questions:
- Consult the official API documentation
- Ask in TrueNAS community forums
- Check TrueNAS release notes for API changes
