# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-03-15

### Added
- Support for Python 3.12.0 and above

## [1.0.0] - 2024-03-15

### Added
- Initial stable release with core functionality
- System dependency management and verification
- Tmux configuration with plugin support
- Tool installation framework
- Support for installing Pretender
- Support for downloading DC enumeration script
- Directory structure management for tools and engagements
- System update and upgrade functionality
- Python version verification
- Color-coded status messages and banner display

### Changed
- Moved Python dependencies (pipx, virtualenv) to system dependencies using apt
- Streamlined dependency installation process
- Enhanced tmux configuration with improved status bar and logging

### Removed
- ZSH environment verification (as it's not needed)
- Network-related tests from test_ez-rta.sh
- Obsolete test script

### Fixed
- Improved error handling in command execution
- Enhanced dependency checking logic
- Better system architecture detection for tool installation

### Security
- Added root privilege verification
- Implemented secure dependency installation checks

### Documentation
- Added comprehensive docstrings to all functions
- Included detailed setup instructions in README
- Added version information to script header

[1.1.0]: https://github.com/yourusername/ez-rta/releases/tag/v1.1.0
[1.0.0]: https://github.com/yourusername/ez-rta/releases/tag/v1.0.0 