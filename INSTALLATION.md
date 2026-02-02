# Installation and Configuration Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [TrueNAS Configuration](#truenas-configuration)
4. [Home Assistant Configuration](#home-assistant-configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### TrueNAS Requirements
- TrueNAS SCALE 22.02 or later (v25.10.2 recommended)
- Administrative access to TrueNAS web interface
- Network connectivity between Home Assistant and TrueNAS
- HTTPS enabled on TrueNAS (default)

### Home Assistant Requirements
- Home Assistant 2023.1 or later
- Custom integration support (default in standard installations)
- Network access to TrueNAS

### Network Requirements
- TrueNAS must be accessible from Home Assistant
- WebSocket support (port 443 by default with HTTPS)
- No firewall blocking between systems

## Installation Methods

### Method 1: HACS Installation (Recommended)

HACS (Home Assistant Community Store) provides the easiest way to install and update the integration.

#### Step 1: Install HACS
If you don't have HACS installed:
1. Visit https://hacs.xyz/docs/setup/download
2. Follow the installation instructions
3. Restart Home Assistant
4. Complete HACS configuration

#### Step 2: Add Custom Repository
1. Open HACS in Home Assistant sidebar
2. Click on **Integrations**
3. Click the three dots (⋮) in the upper right corner
4. Select **Custom repositories**
5. Add repository URL: `https://github.com/tomaae/homeassistant-truenas`
6. Select category: **Integration**
7. Click **Add**

#### Step 3: Install Integration
1. Search for "TrueNAS" in HACS
2. Click on the TrueNAS integration
3. Click **Download**
4. Select the latest version
5. Click **Download** again
6. Restart Home Assistant

### Method 2: Manual Installation

For advanced users or when HACS is not available.

#### Step 1: Download Files
1. Download the latest release from GitHub
2. Extract the ZIP file
3. Locate the `custom_components/truenas` folder

#### Step 2: Copy to Home Assistant
1. Access your Home Assistant configuration directory
2. Create `custom_components` directory if it doesn't exist:
   ```
   homeassistant/
   ├── custom_components/
   │   └── truenas/
   │       ├── __init__.py
   │       ├── manifest.json
   │       ├── api.py
   │       ├── coordinator.py
   │       └── ... (other files)
   └── configuration.yaml
   ```

3. Copy the entire `truenas` folder to `custom_components/`

#### Step 3: Set Permissions
Ensure files are readable by Home Assistant:
```bash
chmod -R 755 custom_components/truenas
```

#### Step 4: Restart Home Assistant
1. Go to **Settings** > **System**
2. Click **Restart** in the top right
3. Confirm restart

## TrueNAS Configuration

### Step 1: Access TrueNAS Web Interface
1. Open your browser
2. Navigate to `https://<truenas-ip-address>`
3. Log in with administrative credentials

### Step 2: Generate API Key

#### For TrueNAS SCALE 24.04+
1. Click on user icon in top right
2. Select **API Keys**
3. Click **Add**
4. Configure the API key:
   - **Name**: `Home Assistant` (or any descriptive name)
   - **Expires**: Set expiration (optional, recommended: 1 year)
   - Click **Add**

5. **Important**: Copy the API key immediately
   - The key will only be shown once
   - Store it securely (e.g., password manager)
   - Click **Close** after copying

#### For Earlier Versions
1. Go to **Credentials** > **Local Users**
2. Find the admin user or create a dedicated user
3. Click on the user
4. Scroll to **API Keys** section
5. Click **Add**
6. Enter a name: `Home Assistant`
7. Click **Save**
8. **Copy the generated API key** (shown only once!)

### Step 3: Verify API Access
Test the API key works:

1. Open browser developer tools (F12)
2. Navigate to TrueNAS at `https://<truenas-ip>/api/docs/`
3. The API documentation should load
4. This confirms the API is accessible

### Optional: SSL Certificate Configuration

For production use, configure a valid SSL certificate:

#### Option 1: Let's Encrypt (Recommended)
1. Go to **Credentials** > **Certificates**
2. Click **Add** > **ACME Certificate**
3. Configure Let's Encrypt settings
4. Complete domain validation
5. Apply certificate to Web UI

#### Option 2: Import Custom Certificate
1. Go to **Credentials** > **Certificates**
2. Click **Add** > **Import Certificate**
3. Upload certificate and private key
4. Apply certificate to Web UI

#### Option 3: Disable SSL Verification (Not Recommended)
If using self-signed certificates, you can disable SSL verification in the Home Assistant integration configuration.

## Home Assistant Configuration

### Step 1: Add Integration
1. In Home Assistant, go to **Settings** > **Devices & Services**
2. Click **Add Integration** (bottom right)
3. Search for "TrueNAS"
4. Select the TrueNAS integration

### Step 2: Configure Connection

Fill in the configuration form:

#### Host
- **Format**: IP address or hostname
- **Examples**: 
  - `192.168.1.100`
  - `truenas.local`
  - `truenas.example.com`
- **Note**: Do not include `http://` or `https://`

#### API Key
- **Value**: Paste the API key generated in TrueNAS
- **Format**: Long alphanumeric string
- **Example**: `1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### Verify SSL Certificate
- **Enabled** (default): Use for valid certificates
  - Let's Encrypt certificates
  - Properly signed certificates
  - Corporate CA certificates

- **Disabled**: Use for self-signed certificates
  - Development environments
  - Self-signed certificates
  - When certificate validation fails

#### Name
- **Default**: Uses TrueNAS hostname
- **Custom**: Enter any friendly name
- **Examples**: "Main Storage", "Backup Server"

### Step 3: Submit Configuration
1. Click **Submit**
2. Wait for connection validation
3. Integration should appear in devices & services

### Step 4: Success Indicators
After successful configuration:
- ✅ Integration appears in Devices & Services
- ✅ TrueNAS device is created
- ✅ Sensors start populating with data
- ✅ No error notifications

## Verification

### Check Integration Status
1. Go to **Settings** > **Devices & Services**
2. Find TrueNAS integration
3. Click on it to view:
   - Device information
   - All entities (sensors, binary sensors, etc.)
   - Diagnostic information

### Verify Sensors

Check that sensors are working:

#### System Sensors
- Navigate to **Developer Tools** > **States**
- Search for `sensor.truenas_`
- Verify sensors show values:
  - `sensor.truenas_system_version`
  - `sensor.truenas_uptime`
  - `sensor.truenas_cpu_usage`
  - `sensor.truenas_memory_usage`

#### Pool Sensors
- Look for pool-related sensors:
  - `sensor.truenas_<pool_name>_status`
  - `sensor.truenas_<pool_name>_used`
  - `sensor.truenas_<pool_name>_available`

### Test Entity Updates
1. Note current value of a sensor
2. Wait 60 seconds (default update interval)
3. Verify sensor value updates
4. Check **Last Updated** timestamp changes

### Check Logs
Review logs for any errors:
1. Go to **Settings** > **System** > **Logs**
2. Search for "truenas"
3. Look for:
   - ✅ "Successfully connected to TrueNAS"
   - ✅ "Data updated successfully"
   - ❌ Error messages (if any)

## Troubleshooting

### Connection Issues

#### Error: "Cannot connect to TrueNAS"
**Possible causes**:
- Incorrect hostname/IP
- Network connectivity issues
- Firewall blocking connection

**Solutions**:
1. Verify TrueNAS is reachable:
   ```bash
   ping <truenas-ip>
   ```
2. Test HTTPS access:
   ```bash
   curl -k https://<truenas-ip>
   ```
3. Check firewall rules on both systems
4. Verify TrueNAS is running

#### Error: "Certificate verification failed"
**Possible causes**:
- Self-signed certificate
- Expired certificate
- Certificate name mismatch

**Solutions**:
1. **Option A**: Disable SSL verification
   - Reconfigure integration
   - Uncheck "Verify SSL Certificate"
   
2. **Option B**: Install valid certificate
   - Use Let's Encrypt
   - Import trusted certificate
   
3. **Option C**: Add certificate to Home Assistant
   - Export TrueNAS certificate
   - Add to Home Assistant trusted certificates

#### Error: "Invalid API key"
**Possible causes**:
- Incorrect API key
- API key revoked
- API key expired

**Solutions**:
1. Regenerate API key in TrueNAS
2. Copy new API key carefully (no extra spaces)
3. Reconfigure integration with new key

### Data Not Updating

#### Sensors Show "Unknown" or "Unavailable"
**Possible causes**:
- Integration not started
- Connection lost
- API permissions issue

**Solutions**:
1. Reload integration:
   - Settings > Devices & Services
   - Click on TrueNAS
   - Click ⋮ > Reload
   
2. Check logs for errors
3. Restart Home Assistant
4. Verify API key still valid

#### Sensors Not Updating (Stale Data)
**Possible causes**:
- Network interruption
- TrueNAS service issues
- WebSocket connection lost

**Solutions**:
1. Check TrueNAS system health
2. Reload integration
3. Restart Home Assistant
4. Check network stability

### Performance Issues

#### Slow Updates
**Possible causes**:
- Large number of datasets
- Slow network connection
- TrueNAS system overload

**Solutions**:
1. Increase update interval (modify coordinator)
2. Reduce number of monitored items
3. Check TrueNAS system performance

### Enabling Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.truenas: debug
    custom_components.truenas.api: debug
    custom_components.truenas.coordinator: debug
```

Restart Home Assistant and check logs:
- Settings > System > Logs
- Filter by "truenas"

### Getting Help

1. **Check Documentation**
   - README.md
   - API_MIGRATION_GUIDE.md
   - This installation guide

2. **Review Logs**
   - Enable debug logging
   - Check for specific error messages
   - Note any patterns

3. **Community Support**
   - Home Assistant Community Forums
   - GitHub Issues
   - Discord channels

4. **Report Issues**
   When reporting issues, include:
   - Home Assistant version
   - TrueNAS version
   - Integration version
   - Relevant log messages
   - Steps to reproduce

## Advanced Configuration

### Custom Update Interval

To change the default 60-second update interval, modify `coordinator.py`:

```python
update_interval=timedelta(seconds=120)  # Change to 120 seconds
```

### Selective Monitoring

To monitor only specific components, modify the `jobs` list in `coordinator.py`.

### Multiple TrueNAS Instances

You can add multiple TrueNAS servers:
1. Add the integration multiple times
2. Each instance requires a unique API key
3. Entities will be prefixed with the server name

## Security Best Practices

### API Key Management
- Generate dedicated API keys per integration
- Rotate API keys periodically (every 6-12 months)
- Revoke unused API keys
- Never commit API keys to version control

### Network Security
- Use firewall rules to limit access
- Enable HTTPS with valid certificates
- Use VPN for remote access
- Keep TrueNAS and Home Assistant updated

### Home Assistant Security
- Secure Home Assistant with authentication
- Use secrets.yaml for sensitive data
- Limit API key permissions if possible
- Monitor integration logs for suspicious activity

## Maintenance

### Regular Tasks
- **Monthly**: Review integration logs for errors
- **Quarterly**: Update integration via HACS
- **Annually**: Rotate API keys

### Updates
1. Check for integration updates in HACS
2. Review changelog for breaking changes
3. Update via HACS
4. Restart Home Assistant
5. Verify functionality

### Backup
Backup your configuration:
- Home Assistant configuration
- API keys (stored securely)
- Custom sensor configurations

## Next Steps

After successful installation:
1. Explore available sensors
2. Create dashboards
3. Set up automations
4. Configure alerts
5. Customize entity names
6. Group related entities

For dashboard examples and automation ideas, see the main README.md.
