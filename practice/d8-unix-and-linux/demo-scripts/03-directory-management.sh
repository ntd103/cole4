#!/bin/bash
# Demo script for Directory Management section

echo "=== Directory Management Demo ==="
echo

# Setup demo environment
cd /demo/data || exit 1

echo "1. Creating Directories:"
echo "Create single directory:"
mkdir projects
echo "Created: projects/"

echo "Create multiple directories:"
mkdir docs temp archive
echo "Created: docs/, temp/, archive/"

echo "Create nested directories:"
mkdir -p projects/web/frontend projects/web/backend
echo "Created: projects/web/frontend/ and projects/web/backend/"
echo

echo "2. Navigating Directories:"
echo "Current directory:"
pwd

echo "Change to projects directory:"
cd projects
pwd

echo "Go back to parent directory:"
cd ..
pwd

echo "Go to home directory:"
cd ~
pwd

echo "Return to demo data directory:"
cd /demo/data
pwd
echo

echo "3. Listing Directory Contents:"
echo "Basic listing:"
ls

echo "Long format listing:"
ls -l

echo "Include hidden files:"
ls -la

echo "Recursive listing:"
ls -R projects/
echo

echo "4. Directory Tree Structure:"
if command -v tree &> /dev/null; then
    echo "Tree view of projects directory:"
    tree projects/
else
    echo "Tree command not available, using ls -R:"
    ls -R projects/
fi
echo

echo "5. Moving Directories:"
echo "Move temp directory into archive:"
mv temp archive/
echo "Directory moved successfully"

echo "Updated structure:"
ls -la
echo

echo "6. Finding Directories:"
echo "Find all directories:"
find . -type d -name "*proj*"
echo

echo "7. Directory Information:"
echo "Disk usage of directories:"
du -h */
echo

echo "=== Directory Management Demo Complete ==="
