#!/bin/bash
# Demo script for Shell Scripting section

echo "=== Shell Scripting Demo ==="
echo

# Ensure we're in the right directory
cd /demo/data || exit 1

echo "1. Basic Script Structure:"
echo "Creating a simple 'Hello World' script:"

cat > hello.sh << 'EOF'
#!/bin/bash
# Simple Hello World script
# Author: Demo User
# Purpose: Demonstrate basic script structure

echo "Hello, World!"
echo "Current date: $(date)"
echo "Current user: $(whoami)"
echo "Script name: $0"
EOF

chmod +x hello.sh
echo "Script created and made executable:"
ls -l hello.sh

echo "Running the script:"
./hello.sh
echo

echo "2. Variables and Input:"
echo "Creating a script that uses variables and user input:"

cat > variables_demo.sh << 'EOF'
#!/bin/bash
# Variables and input demonstration

# Variables
script_name="Variables Demo"
version="1.0"
author="Demo User"

echo "=== $script_name v$version by $author ==="
echo

# Read user input
echo "Enter your name: Demo User"  # Simulated input
name="Demo User"
echo "Enter your age: 25"         # Simulated input
age=25

# Use variables
echo "Hello, $name! You are $age years old."

# Calculate birth year
current_year=$(date +%Y)
birth_year=$((current_year - age))
echo "You were born in approximately $birth_year."

# String operations
echo "Your name in uppercase: ${name^^}"
echo "Your name length: ${#name} characters"
EOF

chmod +x variables_demo.sh
echo "Running variables demo:"
./variables_demo.sh
echo

echo "3. Command Line Arguments:"
echo "Creating a script that processes command line arguments:"

cat > arguments_demo.sh << 'EOF'
#!/bin/bash
# Command line arguments demonstration

echo "Script name: $0"
echo "Number of arguments: $#"
echo "All arguments: $@"

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    echo "Usage: $0 <arg1> <arg2> ..."
    exit 1
fi

echo "Processing arguments:"
for i in $(seq 1 $#); do
    eval arg=\$$i
    echo "  Argument $i: $arg"
done

echo "First argument: $1"
echo "Last argument: ${!#}"
EOF

chmod +x arguments_demo.sh
echo "Running arguments demo with sample arguments:"
./arguments_demo.sh hello world "test argument" 123
echo

echo "4. Functions:"
echo "Creating a script with functions:"

cat > functions_demo.sh << 'EOF'
#!/bin/bash
# Functions demonstration

# Function definition
greet_user() {
    local name="$1"
    local time_of_day="$2"
    
    if [ -z "$name" ]; then
        echo "Good $time_of_day!"
    else
        echo "Good $time_of_day, $name!"
    fi
}

# Function with return value
calculate_area() {
    local length="$1"
    local width="$2"
    local area=$((length * width))
    echo $area
}

# Main script
echo "=== Functions Demo ==="

greet_user "Alice" "morning"
greet_user "Bob" "evening"
greet_user "" "afternoon"

echo
echo "Rectangle area calculation:"
area=$(calculate_area 5 3)
echo "Area of 5x3 rectangle: $area square units"

area=$(calculate_area 10 7)
echo "Area of 10x7 rectangle: $area square units"
EOF

chmod +x functions_demo.sh
echo "Running functions demo:"
./functions_demo.sh
echo

echo "5. Conditional Logic:"
echo "Creating a script with if-else logic:"

cat > conditions_demo.sh << 'EOF'
#!/bin/bash
# Conditional logic demonstration

check_file() {
    local file="$1"
    
    echo "Checking file: $file"
    
    if [ -f "$file" ]; then
        echo "  ✓ File exists"
        
        if [ -r "$file" ]; then
            echo "  ✓ File is readable"
            file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
            echo "  ✓ File size: $file_size bytes"
        else
            echo "  ✗ File is not readable"
        fi
        
        if [ -w "$file" ]; then
            echo "  ✓ File is writable"
        else
            echo "  ✗ File is not writable"
        fi
        
        if [ -x "$file" ]; then
            echo "  ✓ File is executable"
        else
            echo "  ✗ File is not executable"
        fi
    else
        echo "  ✗ File does not exist"
    fi
    echo
}

# Test different files
check_file "hello.sh"
check_file "variables_demo.sh"
check_file "nonexistent.txt"

# Number comparison
echo "Number comparison demo:"
num1=10
num2=20

if [ $num1 -lt $num2 ]; then
    echo "$num1 is less than $num2"
elif [ $num1 -eq $num2 ]; then
    echo "$num1 is equal to $num2"
else
    echo "$num1 is greater than $num2"
fi
EOF

chmod +x conditions_demo.sh
echo "Running conditions demo:"
./conditions_demo.sh
echo

echo "6. Loops:"
echo "Creating a script with different types of loops:"

cat > loops_demo.sh << 'EOF'
#!/bin/bash
# Loops demonstration

echo "=== For Loop Examples ==="

echo "1. Simple for loop with list:"
for fruit in apple banana orange grape; do
    echo "  Fruit: $fruit"
done

echo
echo "2. For loop with range:"
for i in {1..5}; do
    echo "  Number: $i"
done

echo
echo "3. C-style for loop:"
for ((i=1; i<=3; i++)); do
    echo "  Counter: $i"
done

echo
echo "=== While Loop Example ==="
counter=1
while [ $counter -le 3 ]; do
    echo "  While counter: $counter"
    ((counter++))
done

echo
echo "=== Until Loop Example ==="
countdown=3
until [ $countdown -eq 0 ]; do
    echo "  Countdown: $countdown"
    ((countdown--))
done
echo "  Blast off!"

echo
echo "=== Processing Files with Loop ==="
for script_file in *.sh; do
    if [ -f "$script_file" ]; then
        line_count=$(wc -l < "$script_file")
        echo "  $script_file: $line_count lines"
    fi
done
EOF

chmod +x loops_demo.sh
echo "Running loops demo:"
./loops_demo.sh
echo

echo "7. Error Handling:"
echo "Creating a script with error handling:"

cat > error_handling_demo.sh << 'EOF'
#!/bin/bash
# Error handling demonstration

# Enable strict error handling
set -euo pipefail

# Error handling function
handle_error() {
    echo "Error occurred in script at line $1"
    echo "Command that failed: $2"
    exit 1
}

# Trap errors
trap 'handle_error $LINENO "$BASH_COMMAND"' ERR

echo "=== Error Handling Demo ==="

# Function that might fail
risky_operation() {
    local filename="$1"
    
    if [ ! -f "$filename" ]; then
        echo "Warning: File $filename does not exist" >&2
        return 1
    fi
    
    echo "Successfully processed $filename"
    return 0
}

# Test error handling
echo "Testing with existing file:"
if risky_operation "hello.sh"; then
    echo "Operation succeeded"
else
    echo "Operation failed, but script continues"
fi

echo
echo "Testing with non-existent file:"
if risky_operation "nonexistent.txt"; then
    echo "Operation succeeded"
else
    echo "Operation failed, but script continues"
fi

# Disable error trap for this demo
trap - ERR
set +e

echo
echo "Error handling demo completed successfully"
EOF

chmod +x error_handling_demo.sh
echo "Running error handling demo:"
./error_handling_demo.sh
echo

echo "8. Practical Script Example - Backup Utility:"
echo "Creating a practical backup script:"

cat > backup_utility.sh << 'EOF'
#!/bin/bash
# Practical backup utility script

SCRIPT_NAME=$(basename "$0")
BACKUP_DIR="/demo/backup"
LOG_FILE="$BACKUP_DIR/backup.log"

# Logging function
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Help function
show_help() {
    cat << EOF
$SCRIPT_NAME - Simple Backup Utility

Usage: $SCRIPT_NAME [OPTIONS] SOURCE_DIR

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --dest DIR  Specify backup destination (default: $BACKUP_DIR)

Examples:
    $SCRIPT_NAME /demo/data
    $SCRIPT_NAME -v -d /tmp/backup /demo/data
EOF
}

# Parse command line options
VERBOSE=false
SOURCE_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dest)
            BACKUP_DIR="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            SOURCE_DIR="$1"
            shift
            ;;
    esac
done

# Validate input
if [ -z "$SOURCE_DIR" ]; then
    echo "Error: Source directory not specified" >&2
    show_help
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist" >&2
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Perform backup
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_NAME="backup_$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"

log_message "Starting backup of '$SOURCE_DIR'"
log_message "Backup destination: '$BACKUP_PATH'"

if [ "$VERBOSE" = true ]; then
    echo "Verbose mode enabled"
    echo "Creating backup archive..."
fi

# Create compressed backup
if tar -czf "$BACKUP_PATH.tar.gz" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")" 2>/dev/null; then
    BACKUP_SIZE=$(stat -f%z "$BACKUP_PATH.tar.gz" 2>/dev/null || stat -c%s "$BACKUP_PATH.tar.gz" 2>/dev/null)
    log_message "Backup completed successfully"
    log_message "Backup size: $BACKUP_SIZE bytes"
    log_message "Backup file: $BACKUP_PATH.tar.gz"
    
    if [ "$VERBOSE" = true ]; then
        echo "Backup archive contents:"
        tar -tzf "$BACKUP_PATH.tar.gz" | head -10
        if [ $(tar -tzf "$BACKUP_PATH.tar.gz" | wc -l) -gt 10 ]; then
            echo "... and $(( $(tar -tzf "$BACKUP_PATH.tar.gz" | wc -l) - 10 )) more files"
        fi
    fi
else
    log_message "Backup failed"
    exit 1
fi

log_message "Backup operation completed"
EOF

chmod +x backup_utility.sh
echo "Running backup utility demo:"
./backup_utility.sh --help
echo
echo "Creating backup of current directory:"
./backup_utility.sh -v .
echo

echo "9. System Information Script:"
cat > system_info.sh << 'EOF'
#!/bin/bash
# System information gathering script

echo "=== System Information Report ==="
echo "Generated on: $(date)"
echo

echo "--- Basic System Info ---"
echo "Hostname: $(hostname)"
echo "Kernel: $(uname -sr)"
echo "Uptime: $(uptime)"
echo

echo "--- User Information ---"
echo "Current user: $(whoami)"
echo "User ID: $(id -u)"
echo "Group ID: $(id -g)"
echo "Home directory: $HOME"
echo

echo "--- Directory Information ---"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la | head -10

echo
echo "--- Disk Usage ---"
df -h / 2>/dev/null | grep -v "Filesystem"

echo
echo "--- Memory Usage ---"
if command -v free &> /dev/null; then
    free -h
else
    echo "Memory information not available"
fi

echo
echo "--- Process Summary ---"
echo "Total processes: $(ps aux | wc -l)"
echo "Top 3 processes by CPU:"
ps aux --sort=-%cpu | head -4 | tail -3

echo
echo "=== End of Report ==="
EOF

chmod +x system_info.sh
echo "Running system information script:"
./system_info.sh
echo

echo "10. Created Scripts Summary:"
echo "All scripts created in this demo:"
ls -la *.sh | awk '{print $9, $5, $6, $7, $8}' | column -t
echo

echo "=== Shell Scripting Demo Complete ==="

echo
echo "Note: All scripts are now available in /demo/data for further exploration!"
echo "You can run any script by typing: ./script_name.sh"
