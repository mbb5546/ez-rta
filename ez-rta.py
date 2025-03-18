"""
ez-rta.py - Engagement Setup Automation Tool

A comprehensive setup script for penetration testing engagements that:
- Verifies and installs required dependencies
- Configures Tmux environment
- Sets up directory structures for engagements
- Installs and configures common pentesting tools

Table of Contents:
1. Imports and Constants
2. Utility Classes and Functions
   - Colors
   - print_banner
   - print_status
   - run_command

3. System Functions
   - update_system
   - check_python_version

4. Dependency Management
   - install_dependency
   - check_python_package
   - check_core_dependencies
   - verify_tool_installation
   - check_dependencies

5. Environment Configuration
   - setup_tmux

6. Engagement Setup
   - create_engagement_dirs
   - ensure_tools_dir

7. Tool Installation
   - install_pretender
   - download_DC_Enum_Script

8. Main Program Flow
   - main
"""

# ============================================================================
# 1. Imports and Constants
# ============================================================================

import os
import subprocess
import platform
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# 2. Utility Classes and Functions
# ============================================================================

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Prints a colorful banner for the script."""
    # Get current date and time
    current_time = datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S")
    
    banner = f"""
{Colors.YELLOW}{Colors.BOLD}Current Time: {current_time}{Colors.END}

{Colors.CYAN}{Colors.BOLD}  ______  ______       _____  _______        
 |  ____||___  /      |  __ \\|__   __| /\\    
 | |__      / /______ | |__) |  | |   /  \\   
 |  __|    / /|______||  _  /   | |  / /\\ \\  
 | |____  / /__       | | \\ \\   | | / ____ \\ 
 |______|/_____|      |_|  \\_\\  |_|/_/    \\_\\{Colors.END}
                                             
{Colors.BLUE}{Colors.BOLD}[ Engagement Setup Automation Tool ]{Colors.END}
"""
    print(banner)

def print_status(message, status_type="info"):
    """Standardized function for printing status messages."""
    if status_type == "success":
        print(f"{Colors.GREEN}[+] {Colors.WHITE}{message}{Colors.END}")
    elif status_type == "error":
        print(f"{Colors.RED}[-] {Colors.WHITE}{message}{Colors.END}")
    elif status_type == "warning":
        print(f"{Colors.YELLOW}[!] {Colors.WHITE}{message}{Colors.END}")
    elif status_type == "info":
        print(f"{Colors.CYAN}[*] {Colors.WHITE}{message}{Colors.END}")
    else:
        print(message)

def run_command(command, check=True):
    """Runs a shell command and handles errors."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=check, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True  # Capture output as text for easier troubleshooting
        )
        print_status(f"Command executed: {command}", "success")
        return result
    except subprocess.CalledProcessError as e:
        print_status(f"Error running command: {command}\n{e}", "error")
        print_status(f"Command output: {e.stdout}", "error") if e.stdout else None
        print_status(f"Command error: {e.stderr}", "error") if e.stderr else None
        return None

def install_dependency(name, install_command):
    """Attempt to install a missing dependency."""
    print_status(f"Attempting to install {name}...", "info")
    result = run_command(install_command)
    if result and result.returncode == 0:
        print_status(f"Successfully installed {name}", "success")
        return True
    print_status(f"Failed to install {name}. Please install it manually.", "error")
    return False

def check_python_package(package):
    """Check if a Python package is installed."""
    try:
        subprocess.run([sys.executable, "-c", f"import {package}"], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def update_system():
    """Update package lists and upgrade system packages."""
    print_status("Updating system package lists...", "info")
    
    # Update package lists
    result = run_command("apt-get update")
    if not result or result.returncode != 0:
        print_status("Failed to update package lists", "error")
        if input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower() != 'y':
            sys.exit(1)
        return False
    
    print_status("Checking for system upgrades...", "info")
    
    # Check for upgrades
    upgrade_check = run_command("apt-get -s upgrade")
    if upgrade_check and "0 upgraded, 0 newly installed" not in upgrade_check.stdout:
        if input(f"{Colors.YELLOW}System updates are available. Would you like to upgrade? (y/n): {Colors.END}").lower() == 'y':
            result = run_command("apt-get upgrade -y")
            if result and result.returncode == 0:
                print_status("System upgrade completed successfully", "success")
            else:
                print_status("System upgrade failed", "error")
                if input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower() != 'y':
                    sys.exit(1)
    else:
        print_status("System is up to date", "success")
    
    return True

def check_python_version():
    """Check if Python version meets minimum requirements."""
    min_version = (3, 7)
    current_version = sys.version_info[:2]
    
    print_status(f"Checking Python version (minimum required: {min_version[0]}.{min_version[1]})...", "info")
    
    if current_version >= min_version:
        print_status(f"Python version {current_version[0]}.{current_version[1]} meets requirements", "success")
        return True
    else:
        print_status(f"Python version {current_version[0]}.{current_version[1]} is below minimum required version {min_version[0]}.{min_version[1]}", "error")
        return False

def verify_tool_installation(tool_name, check_command):
    """Verify that a tool is properly installed and accessible."""
    try:
        result = subprocess.run(check_command, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_status(f"{tool_name} is properly installed and accessible", "success")
        return True
    except subprocess.CalledProcessError:
        print_status(f"{tool_name} is not properly installed or not accessible", "error")
        return False

def check_core_dependencies():
    """Check and attempt to install core dependencies."""
    # Check Python version
    if not check_python_version():
        if input(f"{Colors.YELLOW}Python version check failed. Continue anyway? (y/n): {Colors.END}").lower() != 'y':
            sys.exit(1)
    
    # Update system packages first
    print_status("Attempting to update system package lists...", "info")
    update_system()
    
    print_status("Checking core dependencies...", "info")
    
    # Core system dependencies
    system_deps = {
        "wget": {"check": "wget --version", "install": "apt-get install -y wget"},
        "git": {"check": "git --version", "install": "apt-get install -y git"},
        "curl": {"check": "curl --version", "install": "apt-get install -y curl"},
        "tmux": {"check": "tmux -V", "install": "apt-get install -y tmux"},
        "zsh": {"check": "zsh --version", "install": "apt-get install -y zsh"},
        # Moving Python dependencies to system deps since we're using apt
        "pipx": {"check": "pipx --version", "install": "apt-get install -y pipx"},
        "virtualenv": {"check": "virtualenv --version", "install": "apt-get install -y python3-virtualenv"}
    }
    
    missing = []
    
    # Check system dependencies
    for name, commands in system_deps.items():
        try:
            subprocess.run(commands["check"], shell=True, check=True, 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_status(f"{name} is installed", "success")
        except subprocess.CalledProcessError:
            missing.append((name, commands["install"]))
            print_status(f"{name} is not installed", "error")
    
    if missing:
        print_status("The following dependencies are missing:", "warning")
        for name, _ in missing:
            print(f"  - {name}")
        
        if input(f"{Colors.YELLOW}Would you like to attempt automatic installation? (y/n): {Colors.END}").lower() == 'y':
            for name, install_cmd in missing:
                install_dependency(name, install_cmd)
        else:
            if input(f"{Colors.YELLOW}Continue without installing dependencies? (y/n): {Colors.END}").lower() != 'y':
                sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed."""
    check_core_dependencies()

def setup_tmux():
    """Creates a Tmux configuration file and installs tmux plugin manager."""
    print_status("Setting up Tmux configuration...", "info")
    
    # Check if tmux is installed
    try:
        subprocess.run("tmux -V", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print_status("Tmux is not installed. Please install it with: apt-get install tmux", "error")
        return False
    
    # Create tmux logs directory
    tmux_logs_path = Path("/root/tmux-logs")
    tmux_logs_path.mkdir(parents=True, exist_ok=True)
    
    # Create tmux configuration
    tmux_conf_path = Path.home() / ".tmux.conf"
    tmux_conf_content = """
# Default Shell
set-option -g default-shell /bin/zsh

# increase history size (Be careful making this too large)
set -g history-limit 30000

# List of plugins
# to enable a plugin, use the 'set -g @plugin' syntax:
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-logging'

# Set logging path
set -g @logging-path "/root/tmux-logs"

# Shift arrow to shift windows
bind -n S-Left previous-window
bind -n S-Right next-window

# set window title list colors
set-window-option -g window-status-style fg=brightblue,bg=colour237,dim

# active window title colors
set-window-option -g window-status-current-style fg=brightgreen,bg=colour237,bright

# show host name and IP address on right side of status bar
set -g status-right-length 70
set -g status-bg colour237
set -g status-fg white
set -g status-right "#[fg=white]Host: #[fg=green]#h#[fg=white] LAN: #[fg=green]#(ip addr show dev eth0 | grep "inet[^6]" | awk '{print $2}')#[fg=white] VPN: #[fg=green]#(ip addr show dev tun0 | grep "inet[^6]" | awk '{print $2}')"

# scroll with mouse
setw -g mouse on
set -g terminal-overrides 'xterm*:smcup@:rmcup@'

# Initialize TMUX plugin manager
run '~/.tmux/plugins/tpm/tpm'
"""
    with open(tmux_conf_path, "w") as f:
        f.write(tmux_conf_content)
    print_status(f"Tmux configuration saved at {tmux_conf_path}", "success")
    print_status(f"Tmux logs will be saved to {tmux_logs_path}", "info")
    
    # Install Tmux Plugin Manager if not already installed
    tpm_path = Path.home() / ".tmux/plugins/tpm"
    if not tpm_path.exists():
        print_status("Installing Tmux Plugin Manager...", "info")
        tpm_cmd = f"git clone https://github.com/tmux-plugins/tpm {tpm_path}"
        result = run_command(tpm_cmd)
        if result and result.returncode == 0:
            print_status("Tmux Plugin Manager installed successfully", "success")
        else:
            print_status("Failed to install Tmux Plugin Manager", "error")
            return False
    else:
        print_status("Tmux Plugin Manager is already installed", "success")
    
    # Add reminder messages
    print_status("\nIMPORTANT: To activate the new tmux configuration:", "info")
    print_status("1. Create a new tmux session: tmux new -s <mysession>", "info")
    print_status("2. Once in tmux, press CTRL+B followed by SHIFT+I to ensure plugins are installed", "info")
    print_status("3. To understand how to use tmux-logging, please refer to the following link: https://github.com/tmux-plugins/tmux-logging", "info")
    print_status("4. Your tmux logs will be saved in /root/tmux-logs", "info")
    return True

# Comment out the create_engagement_dirs function
"""
def create_engagement_dirs():
    #Creates an engagement folder structure.
    print_status("Creating engagement directory structure...", "info")
    base_dir = Path("/root")
    
    # Gather engagement information
    engagement_info = {
        'component': input(f"{Colors.YELLOW}Enter Component Name (e.g., TIPT, CIPT, CPPT): {Colors.END}"),
        'quarter': input(f"{Colors.YELLOW}Enter Quarter (e.g., Q1, Q2, Q3, Q4): {Colors.END}"),
        'initials': input(f"{Colors.YELLOW}Enter Initials (e.g., MB): {Colors.END}"),
        'year': subprocess.run("date +%Y", shell=True, capture_output=True, text=True).stdout.strip()
    }
    
    engagement_dir = base_dir / f"{engagement_info['component']}-{engagement_info['quarter']}-{engagement_info['year']}-{engagement_info['initials']}"
    engagement_info['directory'] = str(engagement_dir)
    
    subdirs = ["nmap", "hosts", "nxc", "loot", "web"]
    for subdir in subdirs:
        (engagement_dir / subdir).mkdir(parents=True, exist_ok=True)
    print_status(f"Engagement directory structure created at {engagement_dir}", "success")
    
    return engagement_info
"""

def ensure_tools_dir():
    """Ensures the tools directory exists at /root/ez-rta-tools."""
    print_status("Ensuring tools directory exists...", "info")
    tools_dir = Path("/root/ez-rta-tools")
    tools_dir.mkdir(parents=True, exist_ok=True)
    print_status(f"Tools directory ensured at {tools_dir}", "success")
    return tools_dir

def install_pretender():
    """Downloads and installs Pretender into a dedicated folder."""
    print_status("Installing Pretender...", "info")
    tools_dir = Path("/root/ez-rta-tools/pretender")
    tools_dir.mkdir(parents=True, exist_ok=True)
    
    # Detect system architecture and OS
    machine = platform.machine().lower()
    system = platform.system().lower()
    
    # Map architecture names
    if machine in ["x86_64", "amd64"]:
        arch = "x86_64"
    elif machine in ["aarch64", "arm64"]:
        arch = "arm64"
    elif "arm" in machine:
        arch = "arm"
    else:
        print_status(f"Unsupported architecture: {machine}. Defaulting to x86_64.", "warning")
        arch = "x86_64"
    
    if system != "linux":
        print_status(f"Unsupported operating system: {system}. The pretender tool requires Linux.", "error")
        return
    
    version = "v1.3.2"  # Using stable version instead of checking GitHub
    
    # Construct the download URL
    pretender_url = f"https://github.com/RedTeamPentesting/pretender/releases/download/{version}/pretender_Linux_{arch}.tar.gz"
    print_status(f"Download URL: {pretender_url}", "info")
    
    pretender_tar = tools_dir / "pretender.tar.gz"
    
    # Download and extract
    result = run_command(f"wget -O {pretender_tar} {pretender_url}")
    if result and result.returncode == 0:
        run_command(f"tar -xzf {pretender_tar} -C {tools_dir}")
        pretender_tar.unlink()
        run_command(f"chmod +x {tools_dir}/pretender")
        
        # Verify installation
        if (tools_dir / "pretender").exists():
            print_status(f"Pretender {version} successfully installed in {tools_dir}", "success")
        else:
            print_status(f"Pretender executable not found after installation. Check for errors.", "error")
    else:
        print_status("Failed to download Pretender", "error")

def download_DC_Enum_Script():
    """Downloads a DC Enumeration script from GitHub."""
    print_status("Downloading DC Enumeration Script...", "info")
    tools_dir = Path("/root/ez-rta-tools")
    repo_url = "https://github.com/mbb5546/dc-lookup.git"
    repo_path = tools_dir / "dc-lookup"
    
    if repo_path.exists():
        print_status("DC Lookup script repository already exists. Pulling latest changes...", "warning")
        result = run_command(f"git -C {repo_path} pull")
    else:
        print_status("Cloning DC Lookup script repository...", "info")
        result = run_command(f"git clone {repo_url} {repo_path}")
    
    if repo_path.exists():
        print_status(f"DC Lookup script downloaded to {repo_path}", "success")
    else:
        print_status("Failed to download DC Lookup script", "error")

def main():
    if os.geteuid() != 0:
        print_status("Please run this script as root.", "error")
        exit(1)

    print_banner()
    
    # Check for dependencies early
    check_dependencies()
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Select which options you'd prefer to skip:{Colors.END}")
    options = {
        "1": ("Create tools directory at /root/ez-rta-tools", ensure_tools_dir),
        "2": ("Install Pretender", install_pretender),
        "3": ("Download DC enumeration script", download_DC_Enum_Script),
        "4": ("Configure Tmux Environment with ZSH as default shell", setup_tmux)
    }

    print(f"\n{Colors.CYAN}Available options:{Colors.END}")
    for key, (desc, _) in options.items():
        print(f"{Colors.BLUE}[{key}]{Colors.END} {desc}")
    
    skip_options = input(f"\n{Colors.YELLOW}Enter the numbers of the options you want to skip, separated by spaces (or press Enter to run all): {Colors.END}").split()

    for key, (desc, func) in options.items():
        if key not in skip_options:
            func()

    print(f"\n${Colors.GREEN}{Colors.BOLD}[+] Setup complete.${Colors.END}")

if __name__ == "__main__":
    main()
