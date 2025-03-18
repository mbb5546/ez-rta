# EZ-RTA (Easy Red Team Automation)

A streamlined automation tool designed to set up and configure penetration testing environments quickly and consistently.

## Overview

EZ-RTA automates the setup of common penetration testing tools and configurations, making it easier to prepare new testing environments. The tool focuses on:

- System dependency management
- Tmux configuration with logging capabilities
- Installation of essential pentesting tools
- Directory structure setup for tools and logging

## Prerequisites

- Root access (sudo privileges)
- Debian-based Linux distribution (tested on Kali Linux)
- Python 3.7 or higher
- Internet connection for initial setup

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ez-rta.git
cd ez-rta
```

2. Run the script with root privileges:
```bash
sudo python3 ez-rta.py
```

## Features

### 1. Dependency Management
- Automatically checks and installs required system dependencies
- Includes: wget, git, curl, tmux, zsh, pipx, virtualenv
- Updates system package lists and offers system upgrades

### 2. Tmux Configuration
- Sets up tmux with ZSH as the default shell
- Configures logging functionality (saves to /root/tmux-logs)
- Installs Tmux Plugin Manager (TPM) with useful plugins
- Customized status bar with system information
- Mouse support enabled
- Enhanced key bindings for better usability

### 3. Tool Installation
- Creates a dedicated tools directory at /root/ez-rta-tools
- Installs Pretender (NTLM relay tool)
- Downloads DC enumeration scripts

## Usage

1. Run the script with root privileges
2. Choose which components to install/configure (or run all)
3. Follow the prompts for any required user input
4. After installation, start a new tmux session:
   ```bash
   tmux new -s mysession
   ```
5. Install tmux plugins by pressing `Ctrl+B` followed by `Shift+I`

## Important Notes and Limitations

### Current Limitations
1. Only tested on Debian-based systems (primarily Kali Linux)
2. Requires root privileges
3. Some features require internet connectivity
4. Tool installations are version-locked (e.g., Pretender v1.3.2)

### Potential Issues
1. Network-dependent operations may fail if connectivity is poor
2. System architecture detection may default to x86_64 if architecture is not recognized
3. Tmux plugin installation requires manual intervention (Ctrl+B, Shift+I)
4. Some system-specific paths are hardcoded (e.g., /root/tmux-logs)

### Error Handling
- The script includes error handling for most operations
- Failed dependency installations will prompt for manual intervention
- System update failures can be bypassed if necessary

## Troubleshooting

### Common Issues
1. If tmux plugins don't load:
   - Verify TPM installation at ~/.tmux/plugins/tpm
   - Manually run: ~/.tmux/plugins/tpm/bin/install_plugins

2. If ZSH isn't working in tmux:
   - Verify zsh installation: `which zsh`
   - Check tmux configuration: `cat ~/.tmux.conf`

3. If tool downloads fail:
   - Verify internet connectivity
   - Check system architecture compatibility
   - Ensure sufficient disk space

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[Insert your chosen license here]

## Acknowledgments

- Tmux Plugin Manager (TPM)
- RedTeamPentesting for Pretender 