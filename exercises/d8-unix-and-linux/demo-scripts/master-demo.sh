#!/bin/bash
# Master demo script that runs all demonstrations

echo "=========================================="
echo "    Unix/Linux Complete Demo Suite"
echo "=========================================="
echo

# Function to run demo with proper formatting
run_demo() {
    local script_name="$1"
    local description="$2"
    
    echo
    echo "==========================================="
    echo "Running: $description"
    echo "Script: $script_name"
    echo "==========================================="
    
    if [ -f "/demo/scripts/$script_name" ]; then
        chmod +x "/demo/scripts/$script_name"
        bash "/demo/scripts/$script_name"
    else
        echo "Error: Script $script_name not found!"
    fi
    
    echo
    read -p "Press Enter to continue to next demo..." -t 10
    echo
}

# Function to show menu
show_menu() {
    echo "Available Demonstrations:"
    echo "1.  Getting Started"
    echo "2.  File Management"
    echo "3.  Directory Management"
    echo "4.  File Permissions"
    echo "5.  Environment Variables"
    echo "6.  Pipes and Filters"
    echo "7.  Process Management"
    echo "8.  Network Utilities"
    echo "9.  Shell Scripting"
    echo "10. Run All Demos"
    echo "11. Exit"
    echo
}

# Main menu loop
while true; do
    show_menu
    read -p "Choose a demo (1-11): " choice
    
    case $choice in
        1)
            run_demo "01-getting-started.sh" "Getting Started with Unix/Linux"
            ;;
        2)
            run_demo "02-file-management.sh" "File Management Operations"
            ;;
        3)
            run_demo "03-directory-management.sh" "Directory Management Operations"
            ;;
        4)
            run_demo "04-file-permissions.sh" "File Permissions and Access Control"
            ;;
        5)
            run_demo "05-environment.sh" "Environment Variables and Configuration"
            ;;
        6)
            run_demo "06-pipes-filters.sh" "Pipes and Filters for Data Processing"
            ;;
        7)
            run_demo "07-process-management.sh" "Process Management and Control"
            ;;
        8)
            run_demo "08-network-utilities.sh" "Network Communication Utilities"
            ;;
        9)
            run_demo "09-shell-scripting.sh" "Shell Scripting and Automation"
            ;;
        10)
            echo "Running all demonstrations..."
            run_demo "01-getting-started.sh" "Getting Started with Unix/Linux"
            run_demo "02-file-management.sh" "File Management Operations"
            run_demo "03-directory-management.sh" "Directory Management Operations"
            run_demo "04-file-permissions.sh" "File Permissions and Access Control"
            run_demo "05-environment.sh" "Environment Variables and Configuration"
            run_demo "06-pipes-filters.sh" "Pipes and Filters for Data Processing"
            run_demo "07-process-management.sh" "Process Management and Control"
            run_demo "08-network-utilities.sh" "Network Communication Utilities"
            run_demo "09-shell-scripting.sh" "Shell Scripting and Automation"
            echo "All demonstrations completed!"
            ;;
        11)
            echo "Exiting demo suite. Thank you!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select 1-11."
            ;;
    esac
done
