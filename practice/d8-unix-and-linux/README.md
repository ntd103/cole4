# Unix/Linux Complete Guide
## A Comprehensive Introduction to Unix/Linux Systems

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [File Management](#file-management)
4. [Directory Management](#directory-management)
5. [File Permissions / Access Modes](#file-permissions--access-modes)
6. [Environment](#environment)
7. [Printing, Email](#printing-email)
8. [Pipes and Filters](#pipes-and-filters)
9. [Process Management](#process-management)
10. [Network Communication Utilities](#network-communication-utilities)
11. [The vi Editor Tutorial](#the-vi-editor-tutorial)
12. [Shell Scripting](#shell-scripting)
13. [What are Shells?](#what-are-shells)
14. [Using Shell Variables](#using-shell-variables)
15. [Special Variables](#special-variables)
16. [Using Shell Arrays](#using-shell-arrays)
17. [Shell Basic Operators](#shell-basic-operators)
18. [Shell Decision Making, Loop](#shell-decision-making-loop)

---

## Prerequisites

### Hardware Requirements
- **Processor**: Any modern CPU (x86, x64, ARM)
- **RAM**: Minimum 512MB (2GB+ recommended)
- **Storage**: 10GB+ free space
- **Network**: Internet connection for updates

### Software Requirements
- Unix/Linux distribution (Ubuntu, CentOS, Debian, etc.)
- Terminal/Console access
- Text editor (vi, nano, emacs)

### Knowledge Prerequisites
- Basic computer operations
- Understanding of file systems
- Familiarity with command-line interfaces
- Basic programming concepts (helpful but not mandatory)

### Learning Objectives
- Navigate Unix/Linux file systems
- Execute commands efficiently
- Manage files and directories
- Understand permissions and security
- Write basic shell scripts
- Use system utilities effectively

---

## Getting Started

### What is Unix/Linux?
Unix is a powerful, multiuser, multitasking operating system originally developed at Bell Labs. Linux is a Unix-like operating system that's open source and widely used.

### Key Features
- **Multiuser**: Multiple users can work simultaneously
- **Multitasking**: Multiple processes can run concurrently
- **Portable**: Runs on various hardware platforms
- **Secure**: Strong security and permission models
- **Hierarchical File System**: Organized tree structure

### Basic Commands
```bash
# Display current date and time
date

# Show current username
whoami

# Display system information
uname -a

# Show current working directory
pwd

# List files and directories
ls

# Clear terminal screen
clear

# Exit terminal session
exit
```

### Command Structure
```
command [options] [arguments]

Examples:
ls -l /home/user
|   |  |
|   |  └── argument (path)
|   └── option (long format)
└── command
```

### Getting Help
```bash
# Manual pages
man command_name
man ls

# Help option
command --help
ls --help

# Information about commands
info command_name

# Which command (location)
which ls

# Type of command
type ls
```

---

## File Management

### Basic File Operations

#### Creating Files
```bash
# Create empty file
touch filename.txt

# Create file with content
echo "Hello World" > file.txt

# Create file using cat
cat > newfile.txt
Type content here
Press Ctrl+D to save

# Copy from another file
cp source.txt destination.txt
```

#### Viewing Files
```bash
# Display entire file
cat filename.txt

# View file page by page
less filename.txt
more filename.txt

# Display first 10 lines
head filename.txt

# Display last 10 lines
tail filename.txt

# Display specific number of lines
head -n 20 filename.txt
tail -n 15 filename.txt

# Follow file changes (useful for logs)
tail -f logfile.txt
```

#### Copying Files
```bash
# Basic copy
cp source.txt destination.txt

# Copy with options
cp -i source.txt dest.txt    # Interactive (prompt before overwrite)
cp -r directory1 directory2  # Recursive (copy directories)
cp -p source.txt dest.txt    # Preserve attributes
cp -v source.txt dest.txt    # Verbose output

# Copy multiple files
cp file1.txt file2.txt file3.txt /destination/directory/
```

#### Moving/Renaming Files
```bash
# Move/rename file
mv oldname.txt newname.txt

# Move to directory
mv file.txt /home/user/documents/

# Move multiple files
mv file1.txt file2.txt /destination/

# Move with options
mv -i file.txt newfile.txt   # Interactive
mv -v file.txt newfile.txt   # Verbose
```

#### Deleting Files
```bash
# Remove file
rm filename.txt

# Remove with confirmation
rm -i filename.txt

# Remove multiple files
rm file1.txt file2.txt file3.txt

# Remove all .tmp files
rm *.tmp

# Force remove (be careful!)
rm -f filename.txt
```

#### File Properties
```bash
# Detailed file information
ls -l filename.txt

# File type information
file filename.txt

# File size
ls -lh filename.txt
du -h filename.txt

# File statistics
stat filename.txt
```

---

## Directory Management

### Creating Directories
```bash
# Create single directory
mkdir directoryname

# Create multiple directories
mkdir dir1 dir2 dir3

# Create parent directories if they don't exist
mkdir -p path/to/new/directory

# Create with specific permissions
mkdir -m 755 directoryname
```

### Navigating Directories
```bash
# Change directory
cd /path/to/directory

# Go to home directory
cd
cd ~

# Go to previous directory
cd -

# Go up one level
cd ..

# Go up multiple levels
cd ../../

# Show current directory
pwd
```

### Listing Directory Contents
```bash
# Basic listing
ls

# Long format
ls -l

# Include hidden files
ls -a

# Long format with hidden files
ls -la

# Sort by modification time
ls -lt

# Reverse order
ls -lr

# Human readable sizes
ls -lh

# Recursive listing
ls -R
```

### Copying Directories
```bash
# Copy directory recursively
cp -r source_directory destination_directory

# Copy with all attributes preserved
cp -rp source_directory destination_directory

# Copy contents only
cp -r source_directory/* destination_directory/
```

### Moving Directories
```bash
# Move/rename directory
mv old_directory new_directory

# Move to another location
mv directory /new/path/

# Move multiple directories
mv dir1 dir2 dir3 /destination/path/
```

### Removing Directories
```bash
# Remove empty directory
rmdir directory_name

# Remove directory and contents (be very careful!)
rm -r directory_name

# Force remove without prompts
rm -rf directory_name

# Remove multiple empty directories
rmdir dir1 dir2 dir3
```

### Finding Files and Directories
```bash
# Find files by name
find /path -name "filename.txt"

# Find directories by name
find /path -type d -name "dirname"

# Find files by extension
find /path -name "*.txt"

# Find files modified in last 7 days
find /path -mtime -7

# Find files larger than 10MB
find /path -size +10M

# Locate command (faster, uses database)
locate filename
```

---

## File Permissions / Access Modes

### Understanding Permissions
Unix/Linux uses a permission system based on three types of users and three types of permissions:

#### User Types:
- **Owner (u)**: The user who owns the file
- **Group (g)**: Users who belong to the file's group
- **Others (o)**: All other users

#### Permission Types:
- **Read (r)**: View file contents or list directory contents
- **Write (w)**: Modify file or create/delete files in directory
- **Execute (x)**: Run file as program or access directory

### Viewing Permissions
```bash
# Long listing shows permissions
ls -l filename.txt
# Output: -rw-r--r-- 1 user group 1024 Jan 15 10:30 filename.txt
#         ||||||||
#         |||||||└── Others permissions
#         ||||||└─── Group permissions  
#         |||||└──── Owner permissions
#         ||||└───── Number of hard links
#         |||└────── File type (- = regular file, d = directory)
```

### Permission Notation
#### Symbolic Notation:
- `rwx`: Read, write, execute
- `r--`: Read only
- `-w-`: Write only
- `--x`: Execute only
- `---`: No permissions

#### Octal Notation:
- Read = 4
- Write = 2
- Execute = 1

Common combinations:
- 7 (4+2+1): rwx (read, write, execute)
- 6 (4+2): rw- (read, write)
- 5 (4+1): r-x (read, execute)
- 4: r-- (read only)
- 0: --- (no permissions)

### Changing Permissions
```bash
# Using symbolic notation
chmod u+x filename.txt        # Add execute for owner
chmod g-w filename.txt        # Remove write for group
chmod o+r filename.txt        # Add read for others
chmod a+r filename.txt        # Add read for all (a=all)

# Using octal notation
chmod 755 filename.txt        # rwxr-xr-x
chmod 644 filename.txt        # rw-r--r--
chmod 600 filename.txt        # rw-------
chmod 777 filename.txt        # rwxrwxrwx (full permissions)

# Recursive permission change
chmod -R 755 directory/       # Apply to directory and contents
```

### Changing Ownership
```bash
# Change owner
chown newowner filename.txt

# Change owner and group
chown newowner:newgroup filename.txt

# Change only group
chgrp newgroup filename.txt

# Recursive ownership change
chown -R newowner:newgroup directory/
```

### Special Permissions
```bash
# Set User ID (SUID) - runs with owner's privileges
chmod u+s filename
chmod 4755 filename

# Set Group ID (SGID) - runs with group's privileges
chmod g+s filename
chmod 2755 filename

# Sticky Bit - only owner can delete (used on directories)
chmod +t directory
chmod 1755 directory
```

### Default Permissions (umask)
```bash
# View current umask
umask

# Set umask (subtract from 777 for directories, 666 for files)
umask 022    # Results in 755 for directories, 644 for files
umask 077    # Results in 700 for directories, 600 for files
```

---

## Environment

### Environment Variables
Environment variables store system and user configuration information.

#### Viewing Environment Variables
```bash
# Display all environment variables
env
printenv

# Display specific variable
echo $HOME
echo $PATH
echo $USER

# Display with additional info
printenv HOME
```

#### Common Environment Variables
```bash
$HOME       # User's home directory
$PATH       # Command search path
$USER       # Current username
$SHELL      # Current shell
$PWD        # Present working directory
$OLDPWD     # Previous working directory
$PS1        # Primary shell prompt
$TERM       # Terminal type
$LANG       # System language
$TZ         # Timezone
```

#### Setting Environment Variables
```bash
# Temporary (current session only)
export MYVAR="Hello World"
export PATH=$PATH:/new/path

# Make permanent (add to shell configuration files)
echo 'export MYVAR="Hello World"' >> ~/.bashrc
echo 'export PATH=$PATH:/new/path' >> ~/.bashrc

# Reload configuration
source ~/.bashrc
```

### Shell Configuration Files
```bash
# System-wide configuration
/etc/profile        # System-wide environment
/etc/bashrc         # System-wide functions and aliases

# User-specific configuration
~/.profile          # User environment (login shells)
~/.bashrc           # User functions and aliases (interactive shells)
~/.bash_profile     # User login shell configuration
~/.bash_logout      # Executed when login shell exits
```

### Aliases
```bash
# Create temporary alias
alias ll='ls -la'
alias grep='grep --color=auto'
alias ..='cd ..'

# Make permanent
echo "alias ll='ls -la'" >> ~/.bashrc

# View all aliases
alias

# Remove alias
unalias ll
```

### History
```bash
# View command history
history

# Execute command from history
!n          # Execute command number n
!!          # Execute last command
!string     # Execute last command starting with string

# History configuration
export HISTSIZE=1000        # Number of commands to remember
export HISTFILESIZE=2000    # Number of lines in history file
```

---

## Printing, Email

### Printing System

#### Basic Printing Commands
```bash
# Print file
lpr filename.txt

# Print with options
lpr -P printer_name filename.txt     # Specify printer
lpr -# 3 filename.txt                # Print 3 copies
lpr -o sides=two-sided filename.txt  # Double-sided printing

# Print from standard input
echo "Hello World" | lpr
```

#### Printer Management
```bash
# List available printers
lpstat -p

# Check print queue
lpq

# Cancel print job
lprm job_number

# Cancel all jobs
lprm -

# Printer status
lpstat -t
```

### Email System

#### Command Line Email
```bash
# Send email using mail command
mail user@domain.com
Subject: Test Email
This is the message body.
Press Ctrl+D to send

# Send email with subject in command line
echo "Message body" | mail -s "Subject" user@domain.com

# Send file as email
mail -s "File Contents" user@domain.com < filename.txt
```

#### Email with Attachments
```bash
# Using mutt (if installed)
mutt -s "Subject" -a attachment.pdf user@domain.com

# Using mail with uuencode
uuencode filename.pdf filename.pdf | mail -s "Subject" user@domain.com
```

#### Reading Email
```bash
# Read email
mail

# Commands within mail:
# h    - list headers
# 1    - read message 1
# d 1  - delete message 1
# q    - quit and save changes
# x    - quit without saving changes
```

---

## Pipes and Filters

### Understanding Pipes
Pipes (|) connect commands, sending output from one command as input to another.

#### Basic Pipe Usage
```bash
# Count lines in file
cat filename.txt | wc -l

# List files and search for pattern
ls -la | grep ".txt"

# Sort file contents
cat names.txt | sort

# Chain multiple commands
cat file.txt | grep "pattern" | sort | uniq
```

### Common Filter Commands

#### grep - Pattern Searching
```bash
# Basic search
grep "pattern" filename.txt

# Case insensitive search
grep -i "pattern" filename.txt

# Show line numbers
grep -n "pattern" filename.txt

# Recursive search in directories
grep -r "pattern" /path/to/directory

# Invert match (show lines that don't match)
grep -v "pattern" filename.txt

# Multiple patterns
grep -E "pattern1|pattern2" filename.txt
```

#### sort - Sorting Lines
```bash
# Basic sort
sort filename.txt

# Reverse sort
sort -r filename.txt

# Numeric sort
sort -n numbers.txt

# Sort by specific field
sort -k 2 filename.txt      # Sort by second field

# Unique sort (remove duplicates)
sort -u filename.txt
```

#### uniq - Remove Duplicates
```bash
# Remove consecutive duplicate lines
uniq filename.txt

# Count occurrences
uniq -c filename.txt

# Show only duplicate lines
uniq -d filename.txt

# Show only unique lines
uniq -u filename.txt
```

#### cut - Extract Columns
```bash
# Extract specific columns
cut -d: -f1,3 /etc/passwd    # Extract fields 1 and 3, delimiter ':'
cut -c 1-10 filename.txt     # Extract characters 1-10

# Extract CSV columns
cut -d, -f2 data.csv
```

#### awk - Pattern Processing
```bash
# Print specific columns
awk '{print $1, $3}' filename.txt

# Process CSV files
awk -F, '{print $2}' data.csv

# Conditional processing
awk '$3 > 100 {print $1, $3}' data.txt

# Calculate sum
awk '{sum += $1} END {print sum}' numbers.txt
```

#### sed - Stream Editor
```bash
# Replace text
sed 's/old/new/' filename.txt           # Replace first occurrence per line
sed 's/old/new/g' filename.txt          # Replace all occurrences

# Delete lines
sed '2d' filename.txt                   # Delete line 2
sed '/pattern/d' filename.txt           # Delete lines containing pattern

# Print specific lines
sed -n '1,5p' filename.txt              # Print lines 1-5
```

### Advanced Pipe Examples
```bash
# Find largest files
ls -la | sort -k 5 -nr | head -10

# Count unique IP addresses in log file
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr

# Monitor system processes
ps aux | grep -v grep | grep process_name

# Network connections summary
netstat -an | grep ESTABLISHED | wc -l
```

---

## Process Management

### Understanding Processes
A process is a running program. Each process has a unique Process ID (PID).

#### Viewing Processes
```bash
# Show all processes
ps aux

# Show processes in tree format
ps auxf
pstree

# Real-time process viewer
top
htop        # Enhanced version (if installed)

# Show specific user processes
ps -u username

# Show processes by name
ps aux | grep process_name
```

#### Process Information
```bash
# Process status columns in ps aux:
# USER    - Process owner
# PID     - Process ID
# %CPU    - CPU usage percentage
# %MEM    - Memory usage percentage
# VSZ     - Virtual memory size
# RSS     - Resident Set Size (physical memory)
# TTY     - Terminal type
# STAT    - Process state
# START   - Start time
# TIME    - CPU time used
# COMMAND - Command that started the process
```

### Starting Processes

#### Foreground and Background
```bash
# Run in foreground (normal)
command

# Run in background
command &

# Send running process to background
Ctrl+Z          # Suspend process
bg              # Continue in background

# Bring background process to foreground
fg              # Bring last job to foreground
fg %1           # Bring job 1 to foreground
```

#### Job Control
```bash
# List active jobs
jobs

# Job states:
# Running   - Currently executing
# Stopped   - Suspended (Ctrl+Z)
# Done      - Completed

# Kill job
kill %1         # Kill job 1
kill %process_name
```

### Terminating Processes

#### Kill Command
```bash
# Terminate process by PID
kill PID

# Different signal types
kill -9 PID     # SIGKILL (forceful termination)
kill -15 PID    # SIGTERM (graceful termination) - default
kill -1 PID     # SIGHUP (hang up)
kill -2 PID     # SIGINT (interrupt, like Ctrl+C)

# Kill by process name
killall process_name
pkill process_name

# Kill all processes by user
killall -u username
```

#### Signal Types
```bash
# Common signals:
# 1  SIGHUP    - Hang up
# 2  SIGINT    - Interrupt (Ctrl+C)
# 9  SIGKILL   - Kill (cannot be caught or ignored)
# 15 SIGTERM   - Terminate (default for kill command)
# 18 SIGCONT   - Continue
# 19 SIGSTOP   - Stop (cannot be caught or ignored)

# List all signals
kill -l
```

### Process Priorities

#### Nice Values
Nice values range from -20 (highest priority) to +19 (lowest priority).

```bash
# Start process with specific nice value
nice -n 10 command

# Change priority of running process
renice -n 5 -p PID

# Start with low priority
nohup nice -n 19 long_running_command &
```

### System Monitoring
```bash
# System load average
uptime
w

# Memory usage
free -h

# Disk usage
df -h
du -h /path/to/directory

# I/O statistics
iostat

# System activity
sar

# Process tree
pstree -p
```

---

## Network Communication Utilities

### Basic Network Commands

#### ping - Test Connectivity
```bash
# Basic ping
ping hostname
ping 8.8.8.8

# Ping with count
ping -c 4 google.com

# Ping with interval
ping -i 2 hostname      # 2 second interval

# Quiet output (summary only)
ping -q -c 4 hostname
```

#### wget - Download Files
```bash
# Download file
wget http://example.com/file.zip

# Download to specific location
wget -O /path/to/save/filename.zip http://example.com/file.zip

# Download recursively
wget -r http://example.com/

# Continue partial download
wget -c http://example.com/largefile.zip

# Background download
wget -b http://example.com/file.zip
```

#### curl - Transfer Data
```bash
# Download and display
curl http://example.com

# Download to file
curl -o filename.html http://example.com

# Follow redirects
curl -L http://example.com

# POST data
curl -X POST -d "data=value" http://example.com/api

# JSON POST
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com
```

### Network Information Commands

#### netstat - Network Connections
```bash
# Show all connections
netstat -a

# Show listening ports
netstat -l

# Show TCP connections
netstat -t

# Show UDP connections
netstat -u

# Show with process information
netstat -p

# Show routing table
netstat -r
```

#### ss - Socket Statistics (modern netstat)
```bash
# Show all connections
ss -a

# Show listening sockets
ss -l

# Show TCP sockets
ss -t

# Show processes
ss -p

# Show specific port
ss -ltn sport = :80
```

#### ifconfig / ip - Network Interface Configuration
```bash
# Show all interfaces
ifconfig
ip addr show

# Show specific interface
ifconfig eth0
ip addr show eth0

# Configure IP address
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0
sudo ip addr add 192.168.1.100/24 dev eth0

# Enable/disable interface
sudo ifconfig eth0 up
sudo ifconfig eth0 down
sudo ip link set eth0 up
sudo ip link set eth0 down
```

### Remote Access Commands

#### ssh - Secure Shell
```bash
# Basic SSH connection
ssh username@hostname

# SSH with specific port
ssh -p 2222 username@hostname

# SSH with key file
ssh -i /path/to/keyfile username@hostname

# Execute command remotely
ssh username@hostname 'ls -la'

# SSH tunneling
ssh -L local_port:remote_host:remote_port username@hostname
```

#### scp - Secure Copy
```bash
# Copy file to remote system
scp localfile username@hostname:/remote/path/

# Copy file from remote system
scp username@hostname:/remote/file /local/path/

# Copy directory recursively
scp -r /local/directory username@hostname:/remote/path/

# Copy with specific port
scp -P 2222 file username@hostname:/path/
```

#### rsync - Remote Synchronization
```bash
# Basic sync
rsync -av /local/path/ username@hostname:/remote/path/

# Sync with delete (mirror)
rsync -av --delete /local/path/ username@hostname:/remote/path/

# Dry run (show what would be transferred)
rsync -avn /local/path/ username@hostname:/remote/path/

# Exclude files
rsync -av --exclude '*.tmp' /local/path/ /backup/path/
```

### DNS Commands

#### nslookup - DNS Lookup
```bash
# Basic lookup
nslookup google.com

# Reverse lookup
nslookup 8.8.8.8

# Specific record type
nslookup -type=MX google.com
```

#### dig - DNS Investigation
```bash
# Basic query
dig google.com

# Specific record type
dig google.com MX
dig google.com NS

# Reverse lookup
dig -x 8.8.8.8

# Short output
dig +short google.com
```

---

## The vi Editor Tutorial

### Introduction to vi
vi (Visual Editor) is a powerful text editor available on virtually all Unix/Linux systems.

### vi Modes
vi operates in three modes:
- **Command Mode**: Default mode for navigation and commands
- **Insert Mode**: For typing text
- **Ex Mode**: For advanced commands and file operations

### Starting vi
```bash
# Open new file
vi filename.txt

# Open existing file
vi /path/to/existing/file.txt

# Open file at specific line
vi +10 filename.txt

# Open file at last line
vi + filename.txt
```

### Mode Switching
```bash
# From Command to Insert Mode:
i    # Insert before cursor
I    # Insert at beginning of line
a    # Insert after cursor
A    # Insert at end of line
o    # Open new line below
O    # Open new line above

# From Insert to Command Mode:
Esc  # Press Escape key

# From Command to Ex Mode:
:    # Type colon

# From Ex to Command Mode:
Esc  # Press Escape key
```

### Navigation (Command Mode)
```bash
# Character movement:
h    # Left
j    # Down
k    # Up
l    # Right

# Word movement:
w    # Next word
b    # Previous word
e    # End of word

# Line movement:
0    # Beginning of line
^    # First non-blank character
$    # End of line

# Screen movement:
Ctrl+f    # Forward one screen
Ctrl+b    # Back one screen
Ctrl+d    # Down half screen
Ctrl+u    # Up half screen

# File movement:
gg   # Go to first line
G    # Go to last line
5G   # Go to line 5
```

### Editing Commands (Command Mode)
```bash
# Deletion:
x    # Delete character under cursor
X    # Delete character before cursor
dw   # Delete word
dd   # Delete line
5dd  # Delete 5 lines
d$   # Delete to end of line
d0   # Delete to beginning of line

# Copying (yanking):
yy   # Copy current line
5yy  # Copy 5 lines
yw   # Copy word
y$   # Copy to end of line

# Pasting:
p    # Paste after cursor/line
P    # Paste before cursor/line

# Undo/Redo:
u    # Undo last change
U    # Undo all changes on current line
Ctrl+r    # Redo
```

### Search and Replace
```bash
# Searching:
/pattern     # Search forward for pattern
?pattern     # Search backward for pattern
n           # Next occurrence
N           # Previous occurrence

# Replace (in Ex mode):
:s/old/new/         # Replace first occurrence in current line
:s/old/new/g        # Replace all occurrences in current line
:%s/old/new/        # Replace first occurrence in each line
:%s/old/new/g       # Replace all occurrences in file
:%s/old/new/gc      # Replace all with confirmation
```

### File Operations (Ex Mode)
```bash
# Saving:
:w              # Save file
:w filename     # Save as filename
:w!             # Force save

# Quitting:
:q              # Quit (if no changes)
:q!             # Quit without saving
:wq             # Save and quit
:x              # Save and quit (same as :wq)
ZZ              # Save and quit (from command mode)

# File information:
:f              # Show filename and position
Ctrl+g          # Show file status
```

### Advanced vi Features
```bash
# Multiple files:
:e filename     # Edit new file
:n              # Next file
:prev           # Previous file

# Windows:
:split          # Horizontal split
:vsplit         # Vertical split
Ctrl+w w        # Switch between windows
Ctrl+w q        # Close current window

# Marks:
ma              # Set mark 'a' at current line
'a              # Go to mark 'a'
''              # Go to previous position

# Macros:
qa              # Start recording macro 'a'
q               # Stop recording
@a              # Play macro 'a'
@@              # Repeat last macro
```

### vi Configuration
```bash
# Set options (temporary):
:set number         # Show line numbers
:set nonumber       # Hide line numbers
:set ignorecase     # Ignore case in searches
:set hlsearch       # Highlight search results
:set tabstop=4      # Set tab width

# Make permanent (add to ~/.vimrc):
echo "set number" >> ~/.vimrc
echo "set tabstop=4" >> ~/.vimrc
echo "set ignorecase" >> ~/.vimrc
```

---

## Shell Scripting

### Introduction to Shell Scripting
Shell scripts are files containing a series of commands that can be executed by the shell. They automate repetitive tasks and create complex workflows.

### Creating Your First Script
```bash
#!/bin/bash
# This is a comment
echo "Hello, World!"
echo "Current date: $(date)"
echo "Current user: $(whoami)"
```

### Script Basics
```bash
# Create script file
vi myscript.sh

# Make executable
chmod +x myscript.sh

# Run script
./myscript.sh
bash myscript.sh
sh myscript.sh
```

### Shebang Line
```bash
#!/bin/bash     # Use bash shell
#!/bin/sh       # Use sh shell (POSIX compatible)
#!/usr/bin/env bash    # Use bash from PATH
```

### Comments and Documentation
```bash
#!/bin/bash
# Script name: backup_script.sh
# Author: Your Name
# Date: 2024-01-15
# Purpose: Backup important files

# This is a single-line comment

: '
This is a
multi-line comment
block
'
```

### Input and Output
```bash
#!/bin/bash

# Display output
echo "Simple text"
echo "Current directory: $(pwd)"

# Read user input
read -p "Enter your name: " name
echo "Hello, $name!"

# Read with timeout
read -t 10 -p "Enter something (10 seconds): " input

# Read password (hidden input)
read -s -p "Enter password: " password
echo  # New line after hidden input
```

### Command Line Arguments
```bash
#!/bin/bash

# Access command line arguments
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"

# Example usage: ./script.sh arg1 arg2 arg3
```

### Exit Codes
```bash
#!/bin/bash

# Exit with success
exit 0

# Exit with error
exit 1

# Check exit code of previous command
if [ $? -eq 0 ]; then
    echo "Previous command succeeded"
else
    echo "Previous command failed"
fi
```

---

## What are Shells?

### Introduction to Shells
A shell is a command-line interpreter that provides a user interface for Unix/Linux operating systems. It acts as an intermediary between the user and the kernel.

### Types of Shells

#### Bourne Shell Family
```bash
# sh - Original Bourne Shell
/bin/sh

# bash - Bourne Again Shell (most common)
/bin/bash

# ksh - Korn Shell
/bin/ksh

# zsh - Z Shell (enhanced features)
/bin/zsh
```

#### C Shell Family
```bash
# csh - C Shell
/bin/csh

# tcsh - TENEX C Shell (enhanced csh)
/bin/tcsh
```

### Shell Features Comparison

| Feature | sh | bash | csh | ksh | zsh |
|---------|----|----- |----- |----- |----- |
| Command History | No | Yes | Yes | Yes | Yes |
| Tab Completion | No | Yes | Limited | Yes | Advanced |
| Aliases | No | Yes | Yes | Yes | Yes |
| Functions | Yes | Yes | No | Yes | Yes |
| Arrays | No | Yes | Yes | Yes | Yes |
| Job Control | No | Yes | Yes | Yes | Yes |

### Checking Your Current Shell
```bash
# Display current shell
echo $SHELL

# Display shell being used by current process
echo $0

# List available shells
cat /etc/shells

# Process information
ps $
```

### Changing Your Shell
```bash
# Temporarily switch shell
bash        # Switch to bash
csh         # Switch to csh
exit        # Return to previous shell

# Permanently change shell
chsh -s /bin/bash       # Change to bash
chsh -s /bin/zsh        # Change to zsh

# Change another user's shell (as root)
chsh -s /bin/bash username
```

### Shell Initialization Files

#### Login vs Non-Login Shells
- **Login Shell**: First shell when you log in
- **Non-Login Shell**: Additional shells opened during session

#### Bash Initialization Order
```bash
# Login Shell:
/etc/profile
~/.bash_profile (or ~/.profile if not found)
~/.bash_login (if ~/.bash_profile not found)

# Non-Login Interactive Shell:
/etc/bashrc (or /etc/bash.bashrc)
~/.bashrc

# Non-Interactive Shell:
$BASH_ENV (if set)
```

### Shell Options
```bash
# Set shell options
set -o option_name

# Common options:
set -o vi           # Vi editing mode
set -o emacs        # Emacs editing mode (default)
set -o noclobber    # Prevent overwriting files with >
set -o nounset      # Error on undefined variables
set -o errexit      # Exit on command failure

# Unset options
set +o option_name

# View all options
set -o
```

---

## Using Shell Variables

### Variable Basics

#### Creating Variables
```bash
# Simple assignment (no spaces around =)
name="John Doe"
age=25
city="New York"

# Using command output
current_date=$(date)
current_user=$(whoami)
file_count=`ls | wc -l`    # Old style - backticks
```

#### Accessing Variables
```bash
# Basic access
echo $name
echo $age

# Using braces (recommended for clarity)
echo ${name}
echo "Hello, ${name}!"

# Concatenation
full_path="${HOME}/${filename}"
greeting="Hello, ${name}. You are ${age} years old."
```

### Variable Types

#### Local Variables
```bash
#!/bin/bash
# Available only in current script/shell
local_var="I'm local"
```

#### Environment Variables
```bash
# Export to make available to child processes
export GLOBAL_VAR="I'm global"

# Or combine declaration and export
export PATH="/new/path:$PATH"
```

#### Read-Only Variables
```bash
# Create read-only variable
readonly PI=3.14159
declare -r CONSTANT="Cannot change"

# Attempt to change will cause error
# PI=3.14    # This will fail
```

### Variable Expansion

#### Basic Expansion
```bash
var="hello"
echo $var           # hello
echo ${var}         # hello
echo "$var world"   # hello world
echo '$var world'   # $var world (no expansion in single quotes)
```

#### Parameter Expansion
```bash
filename="document.txt"

# String length
echo ${#filename}           # 12

# Substring extraction
echo ${filename:0:8}        # document
echo ${filename:9}          # txt

# Remove from beginning
echo ${filename#doc}        # ument.txt
echo ${filename##*.}        # txt (remove everything up to last .)

# Remove from end
echo ${filename%.*}         # document (remove extension)
echo ${filename%%.*}        # document (remove all extensions)
```

#### Default Values
```bash
# Use default if variable is unset or empty
echo ${var:-"default value"}

# Set default if variable is unset or empty
echo ${var:="default value"}

# Use alternate if variable is set and not empty
echo ${var:+"alternate value"}

# Error if variable is unset or empty
echo ${var:?"Variable is required"}
```

### Arrays (Bash)
```bash
# Create array
fruits=("apple" "banana" "orange")
numbers=(1 2 3 4 5)

# Access elements
echo ${fruits[0]}       # apple
echo ${fruits[1]}       # banana

# All elements
echo ${fruits[@]}       # apple banana orange
echo ${fruits[*]}       # apple banana orange

# Array length
echo ${#fruits[@]}      # 3

# Add elements
fruits[3]="grape"
fruits+=("mango")

# Loop through array
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done
```

### Variable Scope
```bash
#!/bin/bash

# Global variable
global_var="I'm global"

function test_scope() {
    # Local variable (only in function)
    local local_var="I'm local"
    
    # Modify global
    global_var="Modified global"
    
    echo "Inside function: $local_var"
    echo "Inside function: $global_var"
}

test_scope
echo "Outside function: $global_var"
# echo "Outside function: $local_var"  # This would be empty
```

---

## Special Variables

### Positional Parameters
```bash
#!/bin/bash
# Script: example.sh

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Third argument: $3"
echo "All arguments: $@"
echo "All arguments (as single word): $*"
echo "Number of arguments: $#"

# Usage: ./example.sh arg1 arg2 arg3
```

### Process-Related Variables
```bash
# Process ID of current shell
echo "Current PID: $"

# Process ID of last background command
command &
echo "Background PID: $!"

# Exit status of last command
ls /nonexistent 2>/dev/null
echo "Exit status: $?"

# Previous working directory
cd /tmp
cd -
echo "Previous directory: $OLDPWD"
```

### System Variables
```bash
# Current working directory
echo "PWD: $PWD"

# Home directory
echo "HOME: $HOME"

# Current user
echo "USER: $USER"
echo "USERNAME: $USERNAME"  # Some systems

# Current shell
echo "SHELL: $SHELL"

# Terminal type
echo "TERM: $TERM"

# System PATH
echo "PATH: $PATH"

# Input Field Separator
echo "IFS: '$IFS'"

# Random number (0-32767)
echo "Random: $RANDOM"

# Seconds since shell started
echo "Seconds: $SECONDS"

# Current line number in script
echo "Line number: $LINENO"
```

### Bash-Specific Variables
```bash
# Bash version
echo "Bash version: $BASH_VERSION"

# Bash process ID
echo "Bash PID: $BASHPID"

# Command history number
echo "History number: $HISTCMD"

# Hostname
echo "Hostname: $HOSTNAME"

# Machine type
echo "Machine type: $MACHTYPE"

# Operating system
echo "OS: $OSTYPE"

# Array of function names
echo "Functions: ${FUNCNAME[@]}"
```

### Using Special Variables in Scripts
```bash
#!/bin/bash

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <source> <destination>"
    exit 1
fi

source_file="$1"
dest_file="$2"

# Check if source file exists
if [ ! -f "$source_file" ]; then
    echo "Error: Source file '$source_file' not found"
    exit 1
fi

# Copy file and check result
cp "$source_file" "$dest_file"
if [ $? -eq 0 ]; then
    echo "File copied successfully"
else
    echo "Copy operation failed"
    exit 1
fi
```

---

## Using Shell Arrays

### Array Declaration (Bash)

#### Different Ways to Create Arrays
```bash
# Method 1: Direct assignment
array[0]="first"
array[1]="second"
array[2]="third"

# Method 2: List assignment
fruits=("apple" "banana" "orange" "grape")

# Method 3: Using declare
declare -a numbers=(1 2 3 4 5)

# Method 4: Empty array
empty_array=()

# Method 5: From command output
files=($(ls *.txt))
users=($(cut -d: -f1 /etc/passwd))
```

### Accessing Array Elements
```bash
fruits=("apple" "banana" "orange")

# Access specific elements
echo ${fruits[0]}       # apple
echo ${fruits[1]}       # banana

# Access all elements
echo ${fruits[@]}       # apple banana orange
echo ${fruits[*]}       # apple banana orange

# Difference between [@] and [*] in quotes
echo "${fruits[@]}"     # "apple" "banana" "orange" (separate words)
echo "${fruits[*]}"     # "apple banana orange" (single word)
```

### Array Properties
```bash
fruits=("apple" "banana" "orange")

# Array length
echo ${#fruits[@]}      # 3
echo ${#fruits[*]}      # 3

# Length of specific element
echo ${#fruits[0]}      # 5 (length of "apple")

# All indices
echo ${!fruits[@]}      # 0 1 2

# Check if element exists
if [[ -v fruits[1] ]]; then
    echo "Element 1 exists: ${fruits[1]}"
fi
```

### Modifying Arrays
```bash
fruits=("apple" "banana")

# Add elements
fruits[2]="orange"                    # Add at specific index
fruits+=("grape")                     # Append single element
fruits+=("mango" "kiwi")             # Append multiple elements

# Modify existing element
fruits[0]="red apple"

# Insert at beginning (recreate array)
fruits=("pear" "${fruits[@]}")

# Remove element (unset)
unset fruits[1]         # Removes "banana" but leaves gap
echo ${fruits[@]}       # red apple orange grape mango kiwi

# Remove last element
unset fruits[-1]        # or unset fruits[${#fruits[@]}-1]
```

### Array Iteration
```bash
fruits=("apple" "banana" "orange")

# Method 1: For loop with elements
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# Method 2: For loop with indices
for i in "${!fruits[@]}"; do
    echo "Index $i: ${fruits[i]}"
done

# Method 3: C-style for loop
for ((i=0; i<${#fruits[@]}; i++)); do
    echo "Item $i: ${fruits[i]}"
done

# Method 4: While loop
i=0
while [ $i -lt ${#fruits[@]} ]; do
    echo "Element $i: ${fruits[i]}"
    ((i++))
done
```

### Associative Arrays (Bash 4+)
```bash
# Declare associative array
declare -A person

# Assign values
person[name]="John Doe"
person[age]="30"
person[city]="New York"

# Access values
echo ${person[name]}        # John Doe
echo ${person[age]}         # 30

# All keys
echo ${!person[@]}          # name age city

# All values
echo ${person[@]}           # John Doe 30 New York

# Iterate through associative array
for key in "${!person[@]}"; do
    echo "$key: ${person[$key]}"
done
```

### Array Operations

#### Slicing Arrays
```bash
numbers=(0 1 2 3 4 5 6 7 8 9)

# Extract slice (start:length)
echo ${numbers[@]:2:3}      # 2 3 4 (start at index 2, take 3 elements)
echo ${numbers[@]:5}        # 5 6 7 8 9 (start at index 5, take rest)

# Negative indices (from end)
echo ${numbers[@]: -3}      # 7 8 9 (last 3 elements)
echo ${numbers[@]: -5:2}    # 5 6 (start 5 from end, take 2)
```

#### Searching Arrays
```bash
fruits=("apple" "banana" "orange" "apple")

# Check if element exists
search="banana"
if [[ " ${fruits[*]} " =~ " ${search} " ]]; then
    echo "Found $search in array"
fi

# Find index of element
search="orange"
for i in "${!fruits[@]}"; do
    if [[ "${fruits[$i]}" == "$search" ]]; then
        echo "Found $search at index $i"
        break
    fi
done
```

#### Sorting Arrays
```bash
fruits=("orange" "apple" "banana")

# Sort array (creates new array)
IFS=\n' sorted_fruits=($(sort <<<"${fruits[*]}"))
unset IFS

echo "Original: ${fruits[@]}"
echo "Sorted: ${sorted_fruits[@]}"

# Sort numerically
numbers=(10 2 30 4)
IFS=\n' sorted_numbers=($(sort -n <<<"${numbers[*]}"))
unset IFS

echo "Numbers: ${numbers[@]}"
echo "Sorted: ${sorted_numbers[@]}"
```

### Practical Array Examples

#### Processing Files
```bash
#!/bin/bash

# Get all .txt files
txt_files=(*.txt)

if [ ${#txt_files[@]} -eq 0 ]; then
    echo "No .txt files found"
    exit 1
fi

echo "Found ${#txt_files[@]} .txt files:"
for file in "${txt_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  $file ($(wc -l < "$file") lines)"
    fi
done
```

#### Menu System
```bash
#!/bin/bash

options=("View files" "Edit file" "Delete file" "Exit")

echo "Select an option:"
for i in "${!options[@]}"; do
    echo "$((i+1)). ${options[i]}"
done

read -p "Enter choice (1-${#options[@]}): " choice

if [[ $choice -ge 1 && $choice -le ${#options[@]} ]]; then
    selected="${options[$((choice-1))]}"
    echo "You selected: $selected"
else
    echo "Invalid choice"
fi
```

---

## Shell Basic Operators

### Arithmetic Operators

#### Basic Arithmetic
```bash
# Using $((...)) - preferred method
a=10
b=3

echo $((a + b))     # Addition: 13
echo $((a - b))     # Subtraction: 7
echo $((a * b))     # Multiplication: 30
echo $((a / b))     # Division: 3 (integer division)
echo $((a % b))     # Modulus: 1
echo $((a ** b))    # Exponentiation: 1000

# Using expr command (older method)
expr $a + $b        # 13
expr $a \* $b       # 30 (escape * in expr)

# Using let command
let result=a+b
echo $result        # 13
```

#### Assignment Operators
```bash
a=10

# Basic assignment
a=5

# Compound assignments (in arithmetic context)
((a += 3))      # a = a + 3 (now 8)
((a -= 2))      # a = a - 2 (now 6)
((a *= 4))      # a = a * 4 (now 24)
((a /= 3))      # a = a / 3 (now 8)
((a %= 5))      # a = a % 5 (now 3)

# Increment/Decrement
((a++))         # Post-increment
((++a))         # Pre-increment
((a--))         # Post-decrement
((--a))         # Pre-decrement
```

### Comparison Operators

#### Numeric Comparisons
```bash
a=10
b=20

# Using test command or [ ]
if [ $a -eq $b ]; then echo "Equal"; fi
if [ $a -ne $b ]; then echo "Not equal"; fi
if [ $a -lt $b ]; then echo "$a less than $b"; fi
if [ $a -le $b ]; then echo "$a less than or equal to $b"; fi
if [ $a -gt $b ]; then echo "$a greater than $b"; fi
if [ $a -ge $b ]; then echo "$a greater than or equal to $b"; fi

# Using (( )) for arithmetic comparison
if ((a == b)); then echo "Equal"; fi
if ((a != b)); then echo "Not equal"; fi
if ((a < b)); then echo "$a less than $b"; fi
if ((a <= b)); then echo "$a less than or equal to $b"; fi
if ((a > b)); then echo "$a greater than $b"; fi
if ((a >= b)); then echo "$a greater than or equal to $b"; fi
```

#### String Comparisons
```bash
str1="hello"
str2="world"
str3="hello"

# String equality
if [ "$str1" = "$str3" ]; then echo "Strings are equal"; fi
if [ "$str1" != "$str2" ]; then echo "Strings are different"; fi

# Lexicographic comparison
if [ "$str1" \< "$str2" ]; then echo "$str1 comes before $str2"; fi
if [ "$str1" \> "$str2" ]; then echo "$str1 comes after $str2"; fi

# String length and emptiness
if [ -z "$str1" ]; then echo "String is empty"; fi
if [ -n "$str1" ]; then echo "String is not empty"; fi

# Pattern matching (bash)
if [[ "$str1" == h* ]]; then echo "String starts with 'h'"; fi
if [[ "$str1" =~ ^h.*o$ ]]; then echo "String matches regex"; fi
```

### Logical Operators

#### Boolean Logic
```bash
a=10
b=20
c=30

# AND operator
if [ $a -lt $b ] && [ $b -lt $c ]; then
    echo "a < b < c"
fi

# OR operator  
if [ $a -eq 10 ] || [ $a -eq 20 ]; then
    echo "a is 10 or 20"
fi

# NOT operator
if ! [ $a -eq $b ]; then
    echo "a is not equal to b"
fi

# Using -a and -o (deprecated but still common)
if [ $a -lt $b -a $b -lt $c ]; then
    echo "a < b < c (old style)"
fi
```

#### Short-Circuit Evaluation
```bash
# && executes second command only if first succeeds
command1 && command2

# || executes second command only if first fails
command1 || command2

# Practical examples
[ -f "file.txt" ] && echo "File exists" || echo "File not found"
cd /some/directory && ls -la || echo "Cannot access directory"
```

### File Test Operators

#### File Existence and Type
```bash
file="/etc/passwd"

if [ -e "$file" ]; then echo "File exists"; fi
if [ -f "$file" ]; then echo "Is a regular file"; fi
if [ -d "$file" ]; then echo "Is a directory"; fi
if [ -L "$file" ]; then echo "Is a symbolic link"; fi
if [ -S "$file" ]; then echo "Is a socket"; fi
if [ -p "$file" ]; then echo "Is a named pipe"; fi
if [ -b "$file" ]; then echo "Is a block device"; fi
if [ -c "$file" ]; then echo "Is a character device"; fi
```

#### File Permissions
```bash
file="/etc/passwd"

if [ -r "$file" ]; then echo "File is readable"; fi
if [ -w "$file" ]; then echo "File is writable"; fi
if [ -x "$file" ]; then echo "File is executable"; fi
if [ -s "$file" ]; then echo "File is not empty"; fi
if [ -O "$file" ]; then echo "You own this file"; fi
if [ -G "$file" ]; then echo "Group owns this file"; fi
```

#### File Comparisons
```bash
file1="/etc/passwd"
file2="/etc/group"

if [ "$file1" -nt "$file2" ]; then echo "file1 is newer than file2"; fi
if [ "$file1" -ot "$file2" ]; then echo "file1 is older than file2"; fi
if [ "$file1" -ef "$file2" ]; then echo "files are the same"; fi
```

### Bitwise Operators
```bash
a=12  # Binary: 1100
b=10  # Binary: 1010

echo $((a & b))     # Bitwise AND: 8 (1000)
echo $((a | b))     # Bitwise OR: 14 (1110)  
echo $((a ^ b))     # Bitwise XOR: 6 (0110)
echo $((~a))        # Bitwise NOT: -13
echo $((a << 2))    # Left shift: 48 (110000)
echo $((a >> 1))    # Right shift: 6 (110)
```

### Operator Precedence
```bash
# Arithmetic operators (highest to lowest precedence)
# 1. () - Parentheses
# 2. ** - Exponentiation
# 3. *, /, % - Multiplication, Division, Modulus
# 4. +, - - Addition, Subtraction
# 5. <<, >> - Bit shifts
# 6. &, |, ^ - Bitwise operations
# 7. ==, !=, <, <=, >, >= - Comparisons
# 8. && - Logical AND
# 9. || - Logical OR

# Examples
result=$((2 + 3 * 4))       # 14 (not 20)
result=$(((2 + 3) * 4))     # 20 (parentheses change order)
```

### Practical Examples

#### Calculator Script
```bash
#!/bin/bash

read -p "Enter first number: " num1
read -p "Enter operator (+, -, *, /, %): " op
read -p "Enter second number: " num2

case $op in
    +) result=$((num1 + num2)) ;;
    -) result=$((num1 - num2)) ;;
    \*) result=$((num1 * num2)) ;;
    /) 
        if [ $num2 -eq 0 ]; then
            echo "Error: Division by zero"
            exit 1
        fi
        result=$((num1 / num2))
        ;;
    %) result=$((num1 % num2)) ;;
    *) echo "Invalid operator"; exit 1 ;;
esac

echo "$num1 $op $num2 = $result"
```

#### File Checker Script
```bash
#!/bin/bash

file="$1"

if [ -z "$file" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

echo "Checking file: $file"

# Existence and type
[ -e "$file" ] && echo "✓ File exists" || echo "✗ File does not exist"
[ -f "$file" ] && echo "✓ Regular file" || echo "- Not a regular file"
[ -d "$file" ] && echo "✓ Directory" || echo "- Not a directory"

# Permissions (if file exists)
if [ -e "$file" ]; then
    [ -r "$file" ] && echo "✓ Readable" || echo "✗ Not readable"
    [ -w "$file" ] && echo "✓ Writable" || echo "✗ Not writable"  
    [ -x "$file" ] && echo "✓ Executable" || echo "✗ Not executable"
    [ -s "$file" ] && echo "✓ Not empty" || echo "- Empty file"
fi
```

---

## Shell Decision Making, Loop

### Conditional Statements

#### if-then-else Structure
```bash
#!/bin/bash

# Basic if statement
if [ condition ]; then
    # commands
fi

# if-else
if [ condition ]; then
    # commands when true
else
    # commands when false
fi

# if-elif-else
if [ condition1 ]; then
    # commands for condition1
elif [ condition2 ]; then
    # commands for condition2
else
    # commands when all conditions false
fi
```

#### Practical if Examples
```bash
#!/bin/bash

# Check file existence
if [ -f "/etc/passwd" ]; then
    echo "Password file exists"
else
    echo "Password file not found"
fi

# Numeric comparison
score=85
if [ $score -ge 90 ]; then
    echo "Grade: A"
elif [ $score -ge 80 ]; then
    echo "Grade: B"
elif [ $score -ge 70 ]; then
    echo "Grade: C"
else
    echo "Grade: F"
fi

# String comparison
read -p "Enter your name: " name
if [ "$name" = "admin" ]; then
    echo "Welcome, administrator!"
elif [ -z "$name" ]; then
    echo "Name cannot be empty"
else
    echo "Hello, $name!"
fi
```

#### case Statement
```bash
#!/bin/bash

# Basic case structure
case $variable in
    pattern1)
        commands1
        ;;
    pattern2)
        commands2
        ;;
    pattern3|pattern4)
        commands3  # Multiple patterns
        ;;
    *)
        default_commands  # Default case
        ;;
esac

# Practical example - Menu system
echo "Select an option:"
echo "1) List files"
echo "2) Show date"
echo "3) Show users"
echo "4) Exit"

read -p "Enter choice: " choice

case $choice in
    1)
        echo "Files in current directory:"
        ls -la
        ;;
    2)
        echo "Current date and time:"
        date
        ;;
    3)
        echo "Logged in users:"
        who
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option"
        ;;
esac
```

### Loop Structures

#### for Loops

##### Traditional for Loop
```bash
#!/bin/bash

# Loop through list of items
for item in apple banana orange; do
    echo "Fruit: $item"
done

# Loop through command output
for file in *.txt; do
    echo "Processing: $file"
done

# Loop through array
fruits=("apple" "banana" "orange")
for fruit in "${fruits[@]}"; do
    echo "Array fruit: $fruit"
done

# Loop through command substitution
for user in $(cut -d: -f1 /etc/passwd); do
    echo "User: $user"
done
```

##### C-style for Loop
```bash
#!/bin/bash

# Basic C-style loop
for ((i=1; i<=10; i++)); do
    echo "Number: $i"
done

# More complex example
for ((i=0, j=10; i<=j; i++, j--)); do
    echo "i=$i, j=$j"
done

# Loop through array indices
array=("a" "b" "c" "d")
for ((i=0; i<${#array[@]}; i++)); do
    echo "Index $i: ${array[i]}"
done
```

#### while Loops
```bash
#!/bin/bash

# Basic while loop
counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Reading file line by line
while read line; do
    echo "Line: $line"
done < filename.txt

# Infinite loop with break condition
while true; do
    read -p "Enter 'quit' to exit: " input
    if [ "$input" = "quit" ]; then
        break
    fi
    echo "You entered: $input"
done

# Menu with while loop
choice=""
while [ "$choice" != "4" ]; do
    echo "1) Option 1"
    echo "2) Option 2" 
    echo "3) Option 3"
    echo "4) Exit"
    read -p "Choose: " choice
    
    case $choice in
        1) echo "You chose option 1" ;;
        2) echo "You chose option 2" ;;
        3) echo "You chose option 3" ;;
        4) echo "Exiting..." ;;
        *) echo "Invalid choice" ;;
    esac
done
```

#### until Loops
```bash
#!/bin/bash

# Basic until loop (opposite of while)
counter=1
until [ $counter -gt 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done

# Wait for file to exist
until [ -f "important_file.txt" ]; do
    echo "Waiting for file..."
    sleep 5
done
echo "File found!"

# Wait for service to be ready
until ping -c 1 google.com &> /dev/null; do
    echo "Waiting for network..."
    sleep 2
done
echo "Network is ready!"
```

### Loop Control

#### break and continue
```bash
#!/bin/bash

# break - exit loop completely
for i in {1..10}; do
    if [ $i -eq 6 ]; then
        echo "Breaking at $i"
        break
    fi
    echo "Number: $i"
done

# continue - skip current iteration
for i in {1..10}; do
    if [ $((i % 2)) -eq 0 ]; then
        continue  # Skip even numbers
    fi
    echo "Odd number: $i"
done

# Nested loops with labeled break
outer_loop=1
while [ $outer_loop -le 3 ]; do
    echo "Outer loop: $outer_loop"
    
    inner_loop=1
    while [ $inner_loop -le 3 ]; do
        if [ $outer_loop -eq 2 ] && [ $inner_loop -eq 2 ]; then
            echo "Breaking inner loop"
            break
        fi
        echo "  Inner loop: $inner_loop"
        ((inner_loop++))
    done
    
    ((outer_loop++))
done
```

### Advanced Control Structures

#### select Loop (Interactive Menu)
```bash
#!/bin/bash

echo "Choose your favorite fruit:"
select fruit in "Apple" "Banana" "Orange" "Quit"; do
    case $fruit in
        "Apple"|"Banana"|"Orange")
            echo "You chose: $fruit"
            ;;
        "Quit")
            echo "Goodbye!"
            break
            ;;
        *)
            echo "Invalid selection"
            ;;
    esac
done
```

#### Functions with Control Structures
```bash
#!/bin/bash

# Function to check if number is prime
is_prime() {
    local num=$1
    local i
    
    if [ $num -lt 2 ]; then
        return 1  # Not prime
    fi
    
    for ((i=2; i*i<=num; i++)); do
        if [ $((num % i)) -eq 0 ]; then
            return 1  # Not prime
        fi
    done
    
    return 0  # Prime
}

# Usage
for num in {1..20}; do
    if is_prime $num; then
        echo "$num is prime"
    fi
done
```

#### Error Handling in Loops
```bash
#!/bin/bash

# Process files with error handling
for file in *.txt; do
    if [ ! -f "$file" ]; then
        echo "Warning: $file not found" >&2
        continue
    fi
    
    if ! cp "$file" "/backup/" 2>/dev/null; then
        echo "Error: Failed to backup $file" >&2
        continue
    fi
    
    echo "Successfully backed up: $file"
done

# Retry mechanism
max_attempts=3
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt of $max_attempts"
    
    if ping -c 1 google.com &>/dev/null; then
        echo "Connection successful!"
        break
    else
        echo "Connection failed"
        if [ $attempt -eq $max_attempts ]; then
            echo "All attempts failed"
            exit 1
        fi
        sleep 5
    fi
    
    ((attempt++))
done
```

### Practical Examples

#### File Processing Script
```bash
#!/bin/bash

# Process all .log files in a directory
log_dir="/var/log"
processed=0
errors=0

if [ ! -d "$log_dir" ]; then
    echo "Error: Directory $log_dir not found"
    exit 1
fi

for log_file in "$log_dir"/*.log; do
    # Skip if no .log files found
    [ ! -f "$log_file" ] && continue
    
    echo "Processing: $(basename "$log_file")"
    
    # Count lines
    line_count=$(wc -l < "$log_file" 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "  Lines: $line_count"
        ((processed++))
        
        # Check for errors in log
        error_count=$(grep -c "ERROR" "$log_file" 2>/dev/null)
        if [ $error_count -gt 0 ]; then
            echo "  Errors found: $error_count"
            ((errors++))
        fi
    else
        echo "  Error: Cannot read file"
        ((errors++))
    fi
done

echo "Summary:"
echo "  Files processed: $processed"
echo "  Files with errors: $errors"
```

#### User Management Script
```bash
#!/bin/bash

# Interactive user management
while true; do
    echo
    echo "User Management System"
    echo "1) List users"
    echo "2) Add user"
    echo "3) Delete user"
    echo "4) User info"
    echo "5) Exit"
    
    read -p "Choose option (1-5): " choice
    
    case $choice in
        1)
            echo "System users:"
            cut -d: -f1 /etc/passwd | sort
            ;;
        2)
            read -p "Enter username: " username
            if id "$username" &>/dev/null; then
                echo "User $username already exists"
            else
                read -p "Create user $username? (y/n): " confirm
                if [ "$confirm" = "y" ]; then
                    if sudo useradd "$username"; then
                        echo "User $username created successfully"
                    else
                        echo "Error creating user $username"
                    fi
                fi
            fi
            ;;
        3)
            read -p "Enter username to delete: " username
            if ! id "$username" &>/dev/null; then
                echo "User $username does not exist"
            else
                read -p "Delete user $username? (y/n): " confirm
                if [ "$confirm" = "y" ]; then
                    if sudo userdel "$username"; then
                        echo "User $username deleted successfully"
                    else
                        echo "Error deleting user $username"
                    fi
                fi
            fi
            ;;
        4)
            read -p "Enter username: " username
            if id "$username" &>/dev/null; then
                echo "User information for $username:"
                id "$username"
                finger "$username" 2>/dev/null || echo "Finger command not available"
            else
                echo "User $username does not exist"
            fi
            ;;
        5)
            echo "Exiting..."
            break
            ;;
        *)
            echo "Invalid option. Please choose 1-5."
            ;;
    esac
    
    read -p "Press Enter to continue..."
done
```

#### Backup Script with Progress
```bash
#!/bin/bash

# Backup script with progress indication
source_dir="$1"
backup_dir="$2"
timestamp=$(date +"%Y%m%d_%H%M%S")

if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_directory> <backup_directory>"
    exit 1
fi

if [ ! -d "$source_dir" ]; then
    echo "Error: Source directory '$source_dir' not found"
    exit 1
fi

mkdir -p "$backup_dir"
backup_path="$backup_dir/backup_$timestamp"

echo "Starting backup from '$source_dir' to '$backup_path'"

# Count total files
echo "Counting files..."
total_files=$(find "$source_dir" -type f | wc -l)
echo "Total files to backup: $total_files"

# Create backup with progress
files_processed=0

find "$source_dir" -type f | while read file; do
    relative_path="${file#$source_dir/}"
    target_dir="$backup_path/$(dirname "$relative_path")"
    
    mkdir -p "$target_dir"
    
    if cp "$file" "$target_dir/"; then
        ((files_processed++))
        progress=$((files_processed * 100 / total_files))
        printf "\rProgress: %d%% (%d/%d files)" $progress $files_processed $total_files
    else
        echo "\nError copying: $file"
    fi
done

echo
echo "Backup completed successfully!"
echo "Backup location: $backup_path"
```

#### System Monitoring Script
```bash
#!/bin/bash

# System monitoring with loops
monitor_duration=300  # 5 minutes
interval=10          # 10 seconds
iterations=$((monitor_duration / interval))

echo "System monitoring starting..."
echo "Duration: ${monitor_duration}s, Interval: ${interval}s"
echo "$(date): Starting monitoring"

for ((i=1; i<=iterations; i++)); do
    echo "--- Sample $i of $iterations ($(date)) ---"
    
    # CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU Usage: ${cpu_usage}%"
    
    # Memory usage
    memory_info=$(free | grep Mem)
    total_mem=$(echo $memory_info | awk '{print $2}')
    used_mem=$(echo $memory_info | awk '{print $3}')
    mem_percent=$((used_mem * 100 / total_mem))
    echo "Memory Usage: ${mem_percent}%"
    
    # Disk usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    echo "Disk Usage: ${disk_usage}%"
    
    # Load average
    load_avg=$(uptime | awk -F'load average:' '{print $2}')
    echo "Load Average: $load_avg"
    
    # Alert conditions
    if [ $cpu_usage -gt 80 ]; then
        echo "ALERT: High CPU usage detected!"
    fi
    
    if [ $mem_percent -gt 80 ]; then
        echo "ALERT: High memory usage detected!"
    fi
    
    if [ $disk_usage -gt 90 ]; then
        echo "ALERT: High disk usage detected!"
    fi
    
    # Wait for next iteration (unless it's the last one)
    if [ $i -lt $iterations ]; then
        sleep $interval
    fi
done

echo "$(date): Monitoring completed"
```

---

## Summary and Best Practices

### Key Takeaways

#### Essential Commands Every Unix/Linux User Should Know
```bash
# Navigation and file operations
pwd, cd, ls, find, locate
cp, mv, rm, mkdir, rmdir
chmod, chown, chgrp

# Text processing
cat, less, more, head, tail
grep, sed, awk, sort, uniq, cut

# System information
ps, top, df, du, free, uname
who, whoami, id, history

# Network utilities
ping, wget, curl, ssh, scp, rsync
```

#### Shell Scripting Best Practices

##### Script Structure
```bash
#!/bin/bash
# Script header with description
# Author, date, purpose

# Set strict mode for better error handling
set -euo pipefail

# Define variables at the top
readonly SCRIPT_NAME=$(basename "$0")
readonly LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"

# Define functions before main logic
function usage() {
    echo "Usage: $SCRIPT_NAME [options] arguments"
    exit 1
}

function log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "$LOG_FILE"
}

# Main script logic
main() {
    # Your code here
    log_message "Script started"
    
    # Always validate input
    if [ $# -eq 0 ]; then
        usage
    fi
    
    log_message "Script completed successfully"
}

# Call main function with all arguments
main "$@"
```

##### Security Considerations
```bash
# Always quote variables to prevent word splitting
if [ -f "$filename" ]; then
    echo "File: $filename"
fi

# Use arrays for multiple items
files=("file1.txt" "file2.txt" "file with spaces.txt")
for file in "${files[@]}"; do
    echo "Processing: $file"
done

# Validate input
read -p "Enter filename: " filename
if [[ ! "$filename" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "Invalid filename"
    exit 1
fi

# Use temporary files securely
temp_file=$(mktemp) || exit 1
trap 'rm -f "$temp_file"' EXIT
```

##### Error Handling
```bash
# Check command success
if ! cp source.txt destination.txt; then
    echo "Error: Failed to copy file" >&2
    exit 1
fi

# Function error handling
function safe_operation() {
    local file="$1"
    
    if [ ! -f "$file" ]; then
        echo "Error: File '$file' not found" >&2
        return 1
    fi
    
    if ! some_command "$file"; then
        echo "Error: Operation failed on '$file'" >&2
        return 1
    fi
    
    return 0
}
```

### Performance Tips

#### Efficient Command Usage
```bash
# Use built-in tests instead of external commands
# Good
if [ -f "$file" ]; then

# Less efficient
if test -f "$file"; then

# Use parameter expansion instead of external commands
# Good
filename="${path##*/}"    # Extract filename

# Less efficient  
filename=$(basename "$path")

# Use here documents for multi-line input
cat << EOF > config.txt
setting1=value1
setting2=value2
EOF
```

#### Memory and Resource Management
```bash
# Process large files line by line
while IFS= read -r line; do
    # Process line
    echo "Processing: $line"
done < largefile.txt

# Use functions to avoid code duplication
function check_file() {
    local file="$1"
    [ -f "$file" ] && [ -r "$file" ]
}

# Cleanup resources
trap 'cleanup' EXIT
function cleanup() {
    [ -f "$temp_file" ] && rm -f "$temp_file"
    [ -d "$temp_dir" ] && rm -rf "$temp_dir"
}
```

### Troubleshooting Common Issues

#### Debug Mode
```bash
# Enable debug output
set -x          # Print commands before execution
set +x          # Disable debug output

# Run script in debug mode
bash -x script.sh

# Add debug output to functions
function debug_function() {
    if [ "${DEBUG:-0}" = "1" ]; then
        echo "DEBUG: $*" >&2
    fi
}

# Usage: DEBUG=1 ./script.sh
```

#### Common Mistakes to Avoid
```bash
# DON'T: Unquoted variables
if [ $var = "value" ]; then    # Fails if var is empty

# DO: Quote variables  
if [ "$var" = "value" ]; then  # Safe

# DON'T: Use ls in scripts
files=$(ls *.txt)              # Fails with spaces in filenames

# DO: Use glob patterns
for file in *.txt; do          # Handles spaces correctly

# DON'T: Parse ls output
for file in $(ls -l | awk '{print $9}'); do

# DO: Use find for complex searches
find . -name "*.txt" -type f | while read -r file; do
```

### Resources for Continued Learning

#### Documentation and References
```bash
# Built-in help
man bash              # Bash manual
info bash             # Bash info pages
help command          # Built-in command help

# Online resources
# - GNU Bash Reference Manual
# - Advanced Bash-Scripting Guide
# - ShellCheck (shellcheck.net) for script validation
# - Bash FAQ and pitfalls
```

#### Practice Exercises
1. Write a script to backup specified directories
2. Create a system monitoring dashboard
3. Build a log file analyzer
4. Implement a file synchronization tool
5. Design an automated deployment script

---

## Conclusion

This comprehensive guide covers the essential aspects of Unix/Linux systems and shell scripting. From basic file operations to advanced scripting techniques, you now have the foundation to work effectively in Unix/Linux environments.

### Next Steps
- Practice the commands and concepts regularly
- Start with simple scripts and gradually increase complexity
- Explore system administration tasks
- Learn about regular expressions for advanced text processing
- Study system security and user management
- Investigate process automation and scheduling (cron)

### Remember
- Always test scripts in a safe environment first
- Use version control for your scripts
- Document your code thoroughly
- Follow security best practices
- Keep learning and exploring new tools and techniques

Unix/Linux mastery comes with practice and experience. Start applying these concepts to real-world scenarios and continue building your expertise in this powerful and versatile operating system environment.