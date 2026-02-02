# TrueNAS Integration for Home Assistant

Monitor and control your TrueNAS SCALE system directly from Home Assistant.

## Features

### System Monitoring
- System version, uptime, and update availability
- CPU usage, load averages, and temperature
- Memory usage (total, used, free, cached, ARC cache)

### Storage
- Pool status, capacity, and health monitoring
- Dataset information and quotas
- Disk status and SMART data
- Boot pool status

### Network
- Interface status and statistics
- Link state and speed
- RX/TX data transfer

### Services & Virtualization
- Service status monitoring (running/stopped)
- Virtual machine status and control
- Application (container) status and monitoring

### Tasks
- Cloud sync task monitoring
- Replication task status
- Snapshot task tracking

## Compatibility

- **TrueNAS SCALE**: v25.10.2 API (backward compatible with earlier versions)
- **Home Assistant**: 2023.1 or later
- **Protocol**: WebSocket API with JSON-RPC 2.0

## Configuration Requirements

You'll need to generate an API key from your TrueNAS SCALE system:
1. Go to **System Settings** > **API Keys**
2. Create a new API key for Home Assistant
3. Copy the key (shown only once)
4. Use it when adding the integration in Home Assistant

## Services

The integration provides services to control your TrueNAS system:
- Start/stop/restart virtual machines and apps
- Run/abort cloud sync jobs
- Create dataset snapshots
- Start/stop/restart/reload services
- Reboot or shutdown TrueNAS system

## Documentation

Full documentation available in the [GitHub repository](https://github.com/sjfehlen/Truenas-HA).

## Support

Report issues on [GitHub Issues](https://github.com/sjfehlen/Truenas-HA/issues).
