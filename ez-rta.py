"""
ez-rta.py - Engagement Setup Automation Tool

A comprehensive setup script for penetration testing engagements that:
- Verifies and installs required dependencies
- Configures ZSH and Tmux environments
- Sets up directory structures for engagements
- Installs and configures common pentesting tools

Table of Contents:
1. Imports and Constants
2. Utility Classes and Functions
   - Colors
   - print_banner
   - print_status
   - run_command

3. System and Network Functions
   - check_internet_connection
   - check_github_access
   - update_system
   - check_python_version

4. Dependency Management
   - install_dependency
   - check_python_package
   - check_core_dependencies
   - verify_tool_installation
   - check_dependencies

5. Environment Configuration
   - update_path_for_pipx
   - verify_zsh_environment
   - setup_tmux

6. Engagement Setup
   - create_engagement_dirs
   - create_tmux_session
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

def check_internet_connection():
    """Check if there is a working internet connection."""
    print_status("Checking internet connectivity...", "info")
    try:
        # Try to connect to a reliable host
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print_status("Internet connection is available", "success")
        return True
    except OSError:
        print_status("No internet connection available", "error")
        return False

def check_github_access():
    """Check if GitHub is accessible."""
    print_status("Checking GitHub accessibility...", "info")
    try:
        urllib.request.urlopen("https://github.com", timeout=5)
        print_status("GitHub is accessible", "success")
        return True
    except:
        print_status("Unable to access GitHub. This may affect tool installations.", "error")
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

def update_path_for_pipx():
    """Update PATH to include pipx installed binaries."""
    print_status("Updating PATH for pipx...", "info")
    
    # Get user's home directory
    home = Path.home()
    pipx_bin_path = home / ".local/bin"
    
    # Check if pipx bin path exists
    if not pipx_bin_path.exists():
        print_status("pipx binary path does not exist. Creating it...", "info")
        pipx_bin_path.mkdir(parents=True, exist_ok=True)
    
    # Add to PATH if not already there
    if str(pipx_bin_path) not in os.environ["PATH"]:
        os.environ["PATH"] = f"{pipx_bin_path}:{os.environ['PATH']}"
        
        # Path export line
        path_export = f'\nexport PATH="{pipx_bin_path}:$PATH"\n'
        
        # Update ZSH config (primary)
        zshrc_path = home / ".zshrc"
        if zshrc_path.exists():
            with open(zshrc_path, 'r') as f:
                content = f.read()
            if str(pipx_bin_path) not in content:
                with open(zshrc_path, 'a') as f:
                    f.write(path_export)
                print_status("Updated .zshrc with pipx PATH", "success")
        else:
            with open(zshrc_path, 'w') as f:
                f.write(path_export)
            print_status("Created .zshrc with pipx PATH", "success")
        
        # Update Bash config (backup)
        bashrc_path = home / ".bashrc"
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                content = f.read()
            if str(pipx_bin_path) not in content:
                with open(bashrc_path, 'a') as f:
                    f.write(path_export)
                print_status("Updated .bashrc with pipx PATH", "success")
        
        # Add pipx completions for zsh
        pipx_completions = """
# pipx completions
eval "$(register-python-argcomplete pipx)"
"""
        if zshrc_path.exists():
            with open(zshrc_path, 'r') as f:
                content = f.read()
            if "register-python-argcomplete pipx" not in content:
                with open(zshrc_path, 'a') as f:
                    f.write(pipx_completions)
                print_status("Added pipx completions to .zshrc", "success")
        
        print_status("Updated PATH to include pipx binaries", "success")
        print_status("Note: You may need to restart your shell or run 'source ~/.zshrc' for PATH changes to take effect", "info")
    else:
        print_status("pipx binary path already in PATH", "success")

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
        "python3-argcomplete": {"check": "dpkg -l python3-argcomplete", "install": "apt-get install -y python3-argcomplete"},
    }
    
    # Python dependencies
    python_deps = {
        "pipx": {"check": "pipx --version", "install": "python3 -m pip install --user pipx"},
        "virtualenv": {"check": "virtualenv --version", "install": "python3 -m pip install --user virtualenv"}
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
    
    # Check Python dependencies
    for name, commands in python_deps.items():
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
                
            # Recheck dependencies after installation attempts
            still_missing = []
            for name, commands in {**system_deps, **python_deps}.items():
                try:
                    subprocess.run(commands["check"], shell=True, check=True, 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    still_missing.append(name)
            
            if still_missing:
                print_status(f"The following dependencies are still missing: {', '.join(still_missing)}", "error")
                if input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower() != 'y':
                    sys.exit(1)
        else:
            if input(f"{Colors.YELLOW}Continue without installing dependencies? (y/n): {Colors.END}").lower() != 'y':
                sys.exit(1)

    # After installing Python dependencies, update PATH
    if any(name == "pipx" for name, _ in missing):
        update_path_for_pipx()
    
    # Verify all installations
    for name, commands in {**system_deps, **python_deps}.items():
        verify_tool_installation(name, commands["check"])

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
    
    # Check if zsh is installed, use bash as fallback
    try:
        subprocess.run("zsh --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        shell_path = "/bin/zsh"
        print_status("Using zsh as default shell in tmux", "success")
    except subprocess.CalledProcessError:
        shell_path = "/bin/bash"
        print_status("Zsh not found, using bash as default shell in tmux", "warning")
    
    # Create tmux configuration
    tmux_conf_path = Path.home() / ".tmux.conf"
    tmux_conf_content = f"""
# Default Shell
set-option -g default-shell {shell_path}

# Increase history size
set -g history-limit 30000

# Plugin list
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-logging'

# Shift arrow to shift windows
bind -n S-Left previous-window
bind -n S-Right next-window

# Scroll with mouse
setw -g mouse on
set -g terminal-overrides 'xterm*:smcup@:rmcup@'

# Initialize TMUX plugin manager
run '~/.tmux/plugins/tpm/tpm'
"""
    with open(tmux_conf_path, "w") as f:
        f.write(tmux_conf_content)
    print_status(f"Tmux configuration saved at {tmux_conf_path}", "success")
    
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
    
    return True

def verify_zsh_environment():
    """Verify that ZSH environment is properly configured."""
    print_status("Verifying ZSH environment...", "info")
    
    home = Path.home()
    zshrc_path = home / ".zshrc"
    
    # Check if ZSH is installed
    try:
        subprocess.run("zsh --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_status("ZSH is installed", "success")
    except subprocess.CalledProcessError:
        print_status("ZSH is not installed", "error")
        if input(f"{Colors.YELLOW}Would you like to install ZSH? (y/n): {Colors.END}").lower() == 'y':
            result = run_command("apt-get install -y zsh")
            if not result or result.returncode != 0:
                print_status("Failed to install ZSH", "error")
                return False
    
    # Check if ZSH is the default shell
    current_shell = os.environ.get('SHELL', '')
    if 'zsh' not in current_shell.lower():
        print_status("ZSH is not the default shell", "warning")
        if input(f"{Colors.YELLOW}Would you like to make ZSH the default shell? (y/n): {Colors.END}").lower() == 'y':
            result = run_command("chsh -s /bin/zsh")
            if result and result.returncode == 0:
                print_status("ZSH set as default shell", "success")
            else:
                print_status("Failed to set ZSH as default shell", "error")
    else:
        print_status("ZSH is the default shell", "success")
    
    # Verify .zshrc exists and has required configurations
    if not zshrc_path.exists():
        print_status(".zshrc file not found, creating it...", "warning")
        with open(zshrc_path, 'w') as f:
            f.write("# Created by ez-rta\n")
    
    # Check for essential configurations
    with open(zshrc_path, 'r') as f:
        content = f.read()
    
    required_configs = {
        'PATH': 'export PATH=',
        'pipx completions': 'register-python-argcomplete pipx'
    }
    
    missing_configs = []
    for config, pattern in required_configs.items():
        if pattern not in content:
            missing_configs.append(config)
    
    if missing_configs:
        print_status(f"Missing configurations in .zshrc: {', '.join(missing_configs)}", "warning")
        return False
    
    print_status("ZSH environment is properly configured", "success")
    return True

def create_tmux_session(engagement_info=None):
    """Create and configure a new tmux session for the engagement."""
    if not engagement_info:
        print_status("No engagement information provided", "error")
        return False
    
    # Create session name from engagement info
    session_name = f"{engagement_info['component']}-{engagement_info['quarter']}-{engagement_info['year']}-{engagement_info['initials']}"
    
    # Check if session already exists
    try:
        subprocess.run(f"tmux has-session -t {session_name}", 
                      shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_status(f"Tmux session '{session_name}' already exists", "warning")
        if input(f"{Colors.YELLOW}Would you like to create a new session with a different name? (y/n): {Colors.END}").lower() == 'y':
            session_name = f"{session_name}-new"
        else:
            return False
    except subprocess.CalledProcessError:
        pass  # Session doesn't exist, which is what we want
    
    # Create the new tmux session
    try:
        # Create session without attaching (-d flag)
        result = run_command(f"tmux new-session -d -s {session_name}")
        if not result or result.returncode != 0:
            print_status(f"Failed to create tmux session '{session_name}'", "error")
            return False
        
        # Configure the session
        commands = [
            # Split window horizontally
            f"tmux split-window -h -t {session_name}",
            # Split right pane vertically
            f"tmux split-window -v -t {session_name}:0.1",
            # Set directory for all panes
            f"tmux send-keys -t {session_name}:0.0 'cd {engagement_info['directory']}' C-m",
            f"tmux send-keys -t {session_name}:0.1 'cd {engagement_info['directory']}' C-m",
            f"tmux send-keys -t {session_name}:0.2 'cd {engagement_info['directory']}' C-m",
            # Select the first pane
            f"tmux select-pane -t {session_name}:0.0"
        ]
        
        for cmd in commands:
            result = run_command(cmd)
            if not result or result.returncode != 0:
                print_status(f"Failed to configure tmux session: {cmd}", "error")
                return False
        
        print_status(f"Tmux session '{session_name}' created and configured", "success")
        print_status(f"To attach to the session, run: tmux attach-session -t {session_name}", "info")
        return True
    
    except Exception as e:
        print_status(f"Error creating tmux session: {str(e)}", "error")
        return False

def create_engagement_dirs():
    """Creates an engagement folder structure."""
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

def ensure_tools_dir():
    """Ensures the tools directory exists and pivots to a new directory if already present."""
    print_status("Ensuring tools directory exists...", "info")
    tools_dir = Path("/root/tools")
    alternate_tools_dir = Path("/root/ez-rta-tools")
    
    if tools_dir.exists():
        print_status(f"{tools_dir} already exists. Using {alternate_tools_dir} instead.", "warning")
        tools_dir = alternate_tools_dir
    
    tools_dir.mkdir(parents=True, exist_ok=True)
    print_status(f"Tools directory ensured at {tools_dir}", "success")
    return tools_dir

def install_pretender():
    """Downloads and installs Pretender into a dedicated folder."""
    print_status("Installing Pretender...", "info")
    tools_dir = Path("/root/tools/pretender")
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
    tools_dir = Path("/root/tools")
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
    
    # Verify ZSH environment
    verify_zsh_environment()
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Select which options you'd prefer to skip:{Colors.END}")
    options = {
        "1": ("Check if /root/tools directory exists. If it does, tools will be moved to /root/ez-rta-tools", ensure_tools_dir),
        "2": ("Install Pretender", install_pretender),
        "3": ("Download DC enumeration script", download_DC_Enum_Script),
        "4": ("Configure Tmux Environment (exclude this option if you prefer screen)", setup_tmux),
        "5": ("Create Engagement Directory Structure and Tmux Session", create_engagement_dirs)
    }

    print(f"\n{Colors.CYAN}Available options:{Colors.END}")
    for key, (desc, _) in options.items():
        print(f"{Colors.BLUE}[{key}]{Colors.END} {desc}")
    
    skip_options = input(f"\n{Colors.YELLOW}Enter the numbers of the options you want to skip, separated by spaces (or press Enter to run all): {Colors.END}").split()

    # Track if tmux was set up successfully and engagement info
    tmux_configured = False
    engagement_info = None
    
    for key, (desc, func) in options.items():
        if key not in skip_options:
            if key == "4":  # Tmux setup
                tmux_configured = func()
            elif key == "5":  # Engagement directory setup
                engagement_info = func()
            else:
                func()

    # Create tmux session if everything is set up
    if tmux_configured and engagement_info:
        create_tmux_session(engagement_info)

    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] Setup complete. Manual steps remaining:{Colors.END}")
    
    # Show tmux instructions
    if tmux_configured and engagement_info:
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Tmux Environment:{Colors.END}")
        print(f"{Colors.WHITE}1. Your tmux session has been created with the name: {engagement_info['component']}-{engagement_info['quarter']}-{engagement_info['year']}-{engagement_info['initials']}")
        print(f"2. To attach to your session, run: tmux attach-session -t {engagement_info['component']}-{engagement_info['quarter']}-{engagement_info['year']}-{engagement_info['initials']}")
        print(f"3. Press Ctrl+B followed by Shift+I to install tmux plugins")
        print(f"4. The session is pre-configured with your engagement directory structure{Colors.END}")

if __name__ == "__main__":
    main()
