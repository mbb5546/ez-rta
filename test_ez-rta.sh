#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}Starting ez-rta.py Testing Suite${NC}"

# Function to run a test case
run_test() {
    local test_name=$1
    local command=$2
    
    echo -e "\n${BLUE}=== Test Case: ${test_name} ===${NC}"
    if eval $command; then
        echo -e "${GREEN}✓ Test Passed: ${test_name}${NC}"
        return 0
    else
        echo -e "${RED}✗ Test Failed: ${test_name}${NC}"
        return 1
    fi
}

# Function to clean environment
clean_env() {
    echo -e "\n${YELLOW}Cleaning test environment...${NC}"
    sudo rm -rf /root/tools /root/ez-rta-tools
    sudo rm -rf /root/*-Q*-202*-*
    sudo rm -f ~/.tmux.conf
    sudo rm -f ~/.zshrc
    sudo killall tmux 2>/dev/null
    echo -e "${GREEN}Environment cleaned${NC}"
}

# Function to check if a package is installed
check_package() {
    dpkg -l "$1" &> /dev/null
}

# Test Categories
test_basic_setup() {
    echo -e "\n${YELLOW}Testing Basic Setup${NC}"
    
    # 1. Non-root execution test
    run_test "Non-root execution (should fail)" "python3 ez-rta.py"
    
    # 2. Root execution test
    run_test "Root execution" "sudo python3 ez-rta.py"
}

test_system_updates() {
    echo -e "\n${YELLOW}Testing System Updates${NC}"
    
    # Test apt update functionality
    run_test "System update check" "sudo apt-get update"
}

test_dependency_management() {
    echo -e "\n${YELLOW}Testing Dependency Management${NC}"
    
    # Remove test dependencies if they exist
    if check_package "tmux"; then
        sudo apt remove -y tmux
    fi
    if check_package "zsh"; then
        sudo apt remove -y zsh
    fi
    
    # Test dependency installation
    run_test "Missing dependencies installation" "echo 'y' | sudo python3 ez-rta.py"
    
    # Verify installations
    run_test "Verify tmux installation" "which tmux"
    run_test "Verify zsh installation" "which zsh"
    run_test "Verify git installation" "which git"
}

test_shell_environment() {
    echo -e "\n${YELLOW}Testing Shell Environment${NC}"
    
    # Test ZSH configuration
    run_test "ZSH environment setup" "echo 'y' | sudo python3 ez-rta.py"
    
    # Verify ZSH configuration
    run_test "Verify .zshrc exists" "test -f ~/.zshrc"
    run_test "Verify PATH in .zshrc" "grep 'export PATH=' ~/.zshrc"
}

test_tmux_setup() {
    echo -e "\n${YELLOW}Testing Tmux Setup${NC}"
    
    # Test tmux configuration
    run_test "Tmux configuration" "echo '4' | sudo python3 ez-rta.py"
    
    # Verify tmux configuration
    run_test "Verify .tmux.conf exists" "test -f ~/.tmux.conf"
    run_test "Verify tmux plugin manager" "test -d ~/.tmux/plugins/tpm"
}

test_directory_structure() {
    echo -e "\n${YELLOW}Testing Directory Structure${NC}"
    
    # Test engagement directory creation
    run_test "Create engagement directory" "echo -e 'TIPT\nQ1\nMB\n' | sudo python3 ez-rta.py"
    
    # Verify directory structure
    run_test "Verify engagement directory exists" "test -d /root/TIPT-Q1-2024-MB"
    run_test "Verify subdirectories exist" "test -d /root/TIPT-Q1-2024-MB/nmap && \
                                          test -d /root/TIPT-Q1-2024-MB/hosts && \
                                          test -d /root/TIPT-Q1-2024-MB/nxc && \
                                          test -d /root/TIPT-Q1-2024-MB/loot && \
                                          test -d /root/TIPT-Q1-2024-MB/web"
}

test_tools_installation() {
    echo -e "\n${YELLOW}Testing Tools Installation${NC}"
    
    # Test tools directory creation
    run_test "Create tools directory" "sudo python3 ez-rta.py"
    
    # Verify tools installation
    run_test "Verify tools directory exists" "test -d /root/tools || test -d /root/ez-rta-tools"
    run_test "Verify Pretender installation" "test -f /root/tools/pretender/pretender || test -f /root/ez-rta-tools/pretender/pretender"
}

# Main testing sequence
main() {
    echo -e "\n${YELLOW}Starting Comprehensive Testing Suite${NC}"
    echo -e "${YELLOW}Note: This script requires root privileges and will modify system state${NC}"
    
    # Initial cleanup
    clean_env
    
    # Run test categories
    test_basic_setup
    test_system_updates
    test_dependency_management
    test_shell_environment
    test_tmux_setup
    test_directory_structure
    test_tools_installation
    
    # Final cleanup
    clean_env
    
    echo -e "\n${GREEN}Testing Complete${NC}"
    echo -e "${YELLOW}Please review the output above for any failures${NC}"
}

# Execute main testing sequence
main 