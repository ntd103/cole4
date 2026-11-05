#!/bin/bash
# Demo script for Getting Started section

echo "=== Unix/Linux Getting Started Demo ==="
echo

# Basic Commands
echo "1. Basic System Information Commands:"
echo "Current date and time:"
date
echo

echo "Current username:"
whoami
echo

echo "System information:"
uname -a
echo

echo "Current working directory:"
pwd
echo

echo "List files and directories:"
ls -la
echo

# Getting Help
echo "2. Getting Help Examples:"
echo "Manual page for 'ls' command:"
man ls | head -20
echo "... (use 'q' to quit man pages)"
echo

echo "Help for 'ls' command:"
ls --help | head -10
echo

echo "Which command shows location:"
which ls
echo

echo "Type command shows command type:"
type ls
echo

# Command Structure Example
echo "3. Command Structure Examples:"
echo "Command: ls -l /home"
echo "  ls     = command"
echo "  -l     = option (long format)"
echo "  /home  = argument (path)"
echo

ls -l /home 2>/dev/null || echo "Directory /home not accessible in container"
echo

echo "=== Getting Started Demo Complete ==="
