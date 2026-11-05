#!/bin/bash
# Demo script for Environment section

echo "=== Environment Demo ==="
echo

echo "1. Viewing Environment Variables:"
echo "Display all environment variables (first 10):"
env | head -10
echo "... (showing first 10 only)"
echo

echo "2. Common Environment Variables:"
echo "HOME directory: $HOME"
echo "Current user: $USER"
echo "Current shell: $SHELL"
echo "Current PATH: $PATH"
echo "Present working directory: $PWD"
echo "Previous working directory: $OLDPWD"
echo "Terminal type: $TERM"
echo "Language setting: $LANG"
echo

echo "3. Setting Environment Variables:"
echo "Setting temporary variable (current session only):"
export DEMO_VAR="Hello from Demo!"
echo "DEMO_VAR = $DEMO_VAR"

echo "Setting PATH variable (adding new path):"
export PATH="$PATH:/demo/scripts"
echo "Updated PATH: $PATH"
echo

echo "4. Shell Configuration Files:"
echo "Checking for common shell configuration files:"
config_files=("$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile" "/etc/profile")

for file in "${config_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ Found: $file"
        echo "  Size: $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "unknown") bytes"
    else
        echo "✗ Not found: $file"
    fi
done
echo

echo "5. Creating and Using Aliases:"
echo "Creating temporary aliases:"
alias ll='ls -la'
alias grep='grep --color=auto'
alias la='ls -A'

echo "Testing aliases:"
echo "ll (same as ls -la):"
ll | head -5

echo "Available aliases:"
alias | grep -E "^(ll|la|grep)="
echo

echo "6. History Configuration:"
echo "History size setting: $HISTSIZE"
echo "History file size: $HISTFILESIZE"
echo "Last 5 commands from history:"
history | tail -5
echo

echo "7. Custom Environment Setup:"
echo "Creating demo environment variables:"
export DEMO_PROJECT="Unix-Linux-Demo"
export DEMO_VERSION="1.0"
export DEMO_AUTHOR="Demo User"
export DEMO_DATE=$(date +%Y-%m-%d)

echo "Demo environment variables:"
echo "  Project: $DEMO_PROJECT"
echo "  Version: $DEMO_VERSION"
echo "  Author: $DEMO_AUTHOR"
echo "  Date: $DEMO_DATE"
echo

echo "8. Environment Variable Scope Demo:"
# Function to demonstrate local vs global variables
function scope_demo() {
    local LOCAL_VAR="I am local"
    GLOBAL_VAR="I am global"
    
    echo "Inside function:"
    echo "  LOCAL_VAR: $LOCAL_VAR"
    echo "  GLOBAL_VAR: $GLOBAL_VAR"
}

echo "Before function call:"
echo "  LOCAL_VAR: ${LOCAL_VAR:-'(not set)'}"
echo "  GLOBAL_VAR: ${GLOBAL_VAR:-'(not set)'}"

scope_demo

echo "After function call:"
echo "  LOCAL_VAR: ${LOCAL_VAR:-'(not set)'}"
echo "  GLOBAL_VAR: ${GLOBAL_VAR:-'(not set)'}"
echo

echo "9. Parameter Expansion Examples:"
filename="document.pdf"
echo "Original filename: $filename"
echo "Length: ${#filename}"
echo "Extension: ${filename##*.}"
echo "Name without extension: ${filename%.*}"
echo "First 8 characters: ${filename:0:8}"
echo

echo "10. Default Values Demo:"
echo "Variable with default value:"
echo "UNSET_VAR with default: ${UNSET_VAR:-'default_value'}"
echo "DEMO_VAR with default: ${DEMO_VAR:-'default_value'}"
echo

echo "=== Environment Demo Complete ==="
