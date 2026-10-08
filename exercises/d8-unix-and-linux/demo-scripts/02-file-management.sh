#!/bin/bash
# Demo script for File Management section

echo "=== File Management Demo ==="
echo

# Setup demo environment
cd /demo/data || exit 1

echo "1. Creating Files:"
echo "Creating empty file with touch:"
touch sample.txt
echo "Created: sample.txt"

echo "Creating file with content using echo:"
echo "Hello, World!" > hello.txt
echo "Created: hello.txt with content"

echo "Creating file with cat:"
cat > story.txt << EOF
Once upon a time,
there was a Unix system.
It was very powerful.
The end.
EOF
echo "Created: story.txt with multiple lines"
echo

echo "2. Viewing Files:"
echo "Display entire file (cat):"
cat hello.txt
echo

echo "Display file with line numbers:"
cat -n story.txt
echo

echo "Display first 2 lines (head):"
head -n 2 story.txt
echo

echo "Display last 2 lines (tail):"
tail -n 2 story.txt
echo

echo "3. Copying Files:"
echo "Copy hello.txt to hello_copy.txt:"
cp hello.txt hello_copy.txt
echo "File copied successfully"

echo "Copy with verbose option:"
cp -v story.txt story_backup.txt
echo

echo "4. Moving/Renaming Files:"
echo "Rename hello_copy.txt to greeting.txt:"
mv hello_copy.txt greeting.txt
echo "File renamed successfully"
echo

echo "5. File Properties:"
echo "Detailed file information:"
ls -l *.txt
echo

echo "File type information:"
file *.txt
echo

echo "File sizes (human readable):"
ls -lh *.txt
echo

echo "6. Current files in directory:"
ls -la
echo

echo "=== File Management Demo Complete ==="
