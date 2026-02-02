# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-02

### Added
- Comprehensive documentation for TrueNAS SCALE v25.10.2 API specifications
- API Migration Guide documenting API changes and usage
- Installation Guide with detailed setup instructions
- API Quick Reference for developers
- Enhanced API client documentation with method descriptions
- Support documentation for all TrueNAS v25.10.2 API endpoints

### Changed
- Updated manifest version to 2.0.0
- Enhanced API.py with comprehensive documentation
- Improved inline documentation throughout codebase
- Updated README with v25.10.2 API compatibility information

### Documented
- system.info - System information endpoint
- interface.query - Network interface queries
- disk.query - Disk information queries
- pool.query - Storage pool queries
- pool.dataset.query - Dataset queries
- virt.instance.query - Virtual machine queries
- app.query - Application queries
- service.query - Service status queries
- cloudsync.query - Cloud sync task queries
- replication.query - Replication task queries
- pool.snapshottask.query - Snapshot task queries
- update.check_available - Update availability checks
- core.get_jobs - Job status queries
- reporting.netdata_get_data - Performance metrics
- disk.temperature_alerts - Disk temperature data
- boot.get_state - Boot pool state

### Technical
- Maintained backward compatibility with previous versions
- Preserved existing functionality
- Enhanced error handling documentation
- Updated WebSocket connection documentation
- Documented JSON-RPC 2.0 protocol usage

### Documentation Structure
- README.md - Main integration documentation
- INSTALLATION.md - Detailed installation guide
- API_MIGRATION_GUIDE.md - API changes and migration information
- API_QUICK_REFERENCE.md - Quick API reference card
- CHANGELOG.md - This file

### Migration Notes
- No breaking changes to existing functionality
- All existing sensors continue to work
- API compatibility maintained
- Configuration remains unchanged
- Direct upgrade from previous versions supported

## [1.x.x] - Previous Versions

See original repository for historical changelog:
https://github.com/tomaae/homeassistant-truenas

---

## Version History

### Understanding Version Numbers

This project follows Semantic Versioning:
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible functionality additions
- **PATCH** version: Backwards-compatible bug fixes

### Upgrade Path

From any 1.x version to 2.0.0:
1. Backup your Home Assistant configuration
2. Update the integration via HACS or manually
3. Restart Home Assistant
4. Verify all sensors are working
5. Review new documentation for enhanced features

### API Compatibility Matrix

| Integration Version | TrueNAS SCALE Version | Status |
|-------------------|---------------------|---------|
| 2.0.0 | 25.10.2 | ✅ Fully Tested |
| 2.0.0 | 25.04.x | ✅ Compatible |
| 2.0.0 | 24.10.x | ✅ Compatible |
| 2.0.0 | 24.04.x | ✅ Compatible |
| 2.0.0 | 23.10.x | ✅ Compatible |
| 2.0.0 | 22.12.x | ✅ Compatible |
| 2.0.0 | 22.02.x | ✅ Compatible |
| 1.x.x | 22.02+ | ✅ Compatible |

### Known Issues

None at this time.

### Future Plans

- Extended sensor coverage for additional TrueNAS features
- Enhanced update entity capabilities
- Additional service controls
- Performance optimizations
- Expanded documentation with examples

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update documentation
5. Submit a pull request

### Support

For support:
- Check documentation in this repository
- Review troubleshooting guides
- Submit issues on GitHub
- Ask in Home Assistant community forums

### Credits

- Original integration: [@tomaae](https://github.com/tomaae)
- TrueNAS SCALE v25.10.2 API update: February 2026
- Contributors: See GitHub repository

### License

This project maintains the original license from the base integration.

---

*Last Updated: February 2, 2026*
