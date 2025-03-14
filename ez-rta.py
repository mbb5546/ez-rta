import os
import subprocess
import platform
import sys
from pathlib import Path
from datetime import datetime

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

def check_dependencies():
    """Check if required dependencies are installed."""
    print_status("Checking for required dependencies...", "info")
    deps = {
        "wget": "wget --version",
        "git": "git --version",
        "curl": "curl --version",
        "tmux": "tmux -V"
    }
    
    missing = []
    for name, command in deps.items():
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print_status(f"{name} is installed", "success")
        except subprocess.CalledProcessError:
            missing.append(name)
            print_status(f"{name} is not installed", "error")
    
    if missing:
        print_status(f"Missing dependencies: {', '.join(missing)}", "error")
        if input(f"{Colors.YELLOW}Continue anyway? (y/n): {Colors.END}").lower() != 'y':
            sys.exit(1)

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

def create_engagement_dirs():
    """Creates an engagement folder structure."""
    print_status("Creating engagement directory structure...", "info")
    base_dir = Path("/root")
    component = input(f"{Colors.YELLOW}Enter Component Name (e.g., TIPT, CIPT, CPPT): {Colors.END}")
    quarter = input(f"{Colors.YELLOW}Enter Quarter (e.g., Q1, Q2, Q3, Q4): {Colors.END}")
    initials = input(f"{Colors.YELLOW}Enter Initials (e.g., MB): {Colors.END}")
    year = subprocess.run("date +%Y", shell=True, capture_output=True, text=True).stdout.strip()
    engagement_dir = base_dir / f"{component}-{quarter}-{year}-{initials}"
    
    subdirs = ["nmap", "hosts", "nxc", "loot", "web"]
    for subdir in subdirs:
        (engagement_dir / subdir).mkdir(parents=True, exist_ok=True)
    print_status(f"Engagement directory structure created at {engagement_dir}", "success")

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
    
    # First, get the latest release info from GitHub
    print_status("Fetching latest release information from GitHub...", "info")
    github_api_url = "https://api.github.com/repos/RedTeamPentesting/pretender/releases/latest"
    
    result = run_command(f"curl -s {github_api_url}")
    if not result or result.returncode != 0:
        print_status("Failed to fetch latest release information. Falling back to v1.3.2.", "warning")
        # Fallback to the known version
        version = "v1.3.2"
    else:
        try:
            # Try to extract the tag_name (version) from the JSON response
            import json
            release_info = json.loads(result.stdout)
            version = release_info.get("tag_name", "v1.3.2")
            print_status(f"Latest version is {version}", "success")
        except:
            print_status("Failed to parse GitHub API response. Falling back to v1.3.2.", "warning")
            version = "v1.3.2"
    
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
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Select which options you'd prefer to skip:{Colors.END}")
    options = {
        "1": ("Check if /root/tools directory exists. If it does, tools will be moved to /root/ez-rta-tools", ensure_tools_dir),
        "2": ("Install Pretender", install_pretender),
        "3": ("Download DC enumeration script", download_DC_Enum_Script),
        "4": ("Configure Tmux Environment (exclude this option if you prefer screen)", setup_tmux),
        "5": ("Create Engagement Directory Structure", create_engagement_dirs)
    }

    print(f"\n{Colors.CYAN}Available options:{Colors.END}")
    for key, (desc, _) in options.items():
        print(f"{Colors.BLUE}[{key}]{Colors.END} {desc}")
    
    skip_options = input(f"\n{Colors.YELLOW}Enter the numbers of the options you want to skip, separated by spaces (or press Enter to run all): {Colors.END}").split()

    # Track if tmux was set up successfully
    tmux_configured = False
    
    for key, (desc, func) in options.items():
        if key not in skip_options:
            if key == "4":  # Tmux setup
                tmux_configured = func()
            else:
                func()

    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] Setup complete. Manual steps remaining:{Colors.END}")
    
    # Only show engagement directory step if not skipped
    if "5" not in skip_options:
        print(f"{Colors.WHITE}1. Begin your engagement in the newly created directory.{Colors.END}")
    
    # Show tmux instructions at the very end if it was configured
    if tmux_configured:
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Tmux Setup Instructions:{Colors.END}")
        print(f"{Colors.WHITE}1. Start a new tmux session with 'tmux new -s <session_name>' command")
        print(f"2. Press Ctrl+B followed by Shift+I to install tmux plugins")
        print(f"3. Restart tmux by exiting (Ctrl+B then d) and starting again{Colors.END}")

if __name__ == "__main__":
    main()
