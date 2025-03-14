#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test results storage
declare -A test_results
declare -A test_messages

echo -e "${YELLOW}Starting ez-rta.py Testing Suite${NC}"

# Function to run a test case and store results
run_test() {
    local test_category=$1
    local test_name=$2
    local command=$3
    
    echo -e "\n${BLUE}=== Testing: ${test_name} ===${NC}"
    if eval $command; then
        echo -e "${GREEN}✓ Test Passed: ${test_name}${NC}"
        test_results["${test_category}:${test_name}"]="PASS"
        test_messages["${test_category}:${test_name}"]="No issues found"
        return 0
    else
        echo -e "${RED}✗ Test Failed: ${test_name}${NC}"
        test_results["${test_category}:${test_name}"]="FAIL"
        test_messages["${test_category}:${test_name}"]="Command failed: $command"
        return 1
    fi
}

# Function to print test summary
print_summary() {
    echo -e "\n${YELLOW}========== TEST SUMMARY ==========${NC}"
    echo -e "${CYAN}Test Date: $(date)${NC}"
    echo -e "${CYAN}System Info: $(uname -a)${NC}"
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Print results by category
    local current_category=""
    for test in "${!test_results[@]}"; do
        category=$(echo $test | cut -d':' -f1)
        test_name=$(echo $test | cut -d':' -f2)
        
        if [ "$current_category" != "$category" ]; then
            echo -e "\n${YELLOW}$category${NC}"
            current_category=$category
        fi
        
        if [ "${test_results[$test]}" == "PASS" ]; then
            echo -e "${GREEN}✓ $test_name${NC}"
            ((passed_tests++))
        else
            echo -e "${RED}✗ $test_name${NC}"
            echo -e "${RED}  └─ Error: ${test_messages[$test]}${NC}"
            ((failed_tests++))
        fi
        ((total_tests++))
    done
    
    # Print statistics
    echo -e "\n${YELLOW}========== STATISTICS ==========${NC}"
    echo -e "Total Tests: $total_tests"
    echo -e "${GREEN}Passed: $passed_tests${NC}"
    echo -e "${RED}Failed: $failed_tests${NC}"
    echo -e "Success Rate: $(( (passed_tests * 100) / total_tests ))%"
    
    # Save summary to file
    echo "========== TEST SUMMARY ==========
Test Date: $(date)
System Info: $(uname -a)

Statistics:
-----------
Total Tests: $total_tests
Passed: $passed_tests
Failed: $failed_tests
Success Rate: $(( (passed_tests * 100) / total_tests ))%

Detailed Results:
----------------" > test_summary.txt
    
    current_category=""
    for test in "${!test_results[@]}"; do
        category=$(echo $test | cut -d':' -f1)
        test_name=$(echo $test | cut -d':' -f2)
        
        if [ "$current_category" != "$category" ]; then
            echo -e "\n$category:" >> test_summary.txt
            current_category=$category
        fi
        
        if [ "${test_results[$test]}" == "PASS" ]; then
            echo "✓ $test_name" >> test_summary.txt
        else
            echo "✗ $test_name" >> test_summary.txt
            echo "  └─ Error: ${test_messages[$test]}" >> test_summary.txt
        fi
    done
    
    echo -e "\n${YELLOW}Summary saved to test_summary.txt${NC}"
}

# Function to clean environment
clean_env() {
    echo -e "\n${YELLOW}Cleaning test environment...${NC}"
    sudo rm -rf /root/ez-rta-tools
    sudo rm -f ~/.tmux.conf
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
    run_test "Basic Setup" "Non-root execution check" "! python3 ez-rta.py"
    run_test "Basic Setup" "Root execution check" "sudo python3 ez-rta.py"
}

test_system_updates() {
    echo -e "\n${YELLOW}Testing System Updates${NC}"
    run_test "System Updates" "APT update functionality" "sudo apt-get update"
}

test_dependency_management() {
    echo -e "\n${YELLOW}Testing Dependency Management${NC}"
    
    # Test core dependencies
    run_test "Dependencies" "Python version check" "python3 --version"
    run_test "Dependencies" "Git installation" "which git"
    run_test "Dependencies" "Wget installation" "which wget"
    run_test "Dependencies" "Curl installation" "which curl"
    
    # Test Python packages
    run_test "Python Packages" "Pipx availability" "which pipx || true"
    run_test "Python Packages" "Virtualenv availability" "which virtualenv || true"
}

test_tmux_setup() {
    echo -e "\n${YELLOW}Testing Tmux Setup${NC}"
    run_test "Tmux" "Tmux installation" "which tmux"
    run_test "Tmux" "Tmux config existence" "test -f ~/.tmux.conf"
    run_test "Tmux" "Tmux plugin manager" "test -d ~/.tmux/plugins/tpm"
    run_test "Tmux" "ZSH shell configuration" "grep 'set-option -g default-shell /bin/zsh' ~/.tmux.conf"
}

test_tools_installation() {
    echo -e "\n${YELLOW}Testing Tools Installation${NC}"
    run_test "Tools" "Tools directory existence" "test -d /root/ez-rta-tools"
    run_test "Tools" "Pretender installation" "test -f /root/ez-rta-tools/pretender/pretender"
    run_test "Tools" "DC-Lookup script" "test -d /root/ez-rta-tools/dc-lookup"
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
    test_tmux_setup
    test_tools_installation
    
    # Generate and display summary
    print_summary
    
    # Final cleanup
    clean_env
}

# Execute main testing sequence
main 