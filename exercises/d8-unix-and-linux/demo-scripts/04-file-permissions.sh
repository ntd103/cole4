#!/bin/bash
# Demo script for File Permissions section

echo "=== File Permissions Demo ==="
echo

# Setup demo environment
cd /demo/data || exit 1

# Create test files if they don't exist
touch test_file.txt
echo "This is a test file for permissions demo" > test_file.txt
mkdir -p test_directory

echo "1. Viewing Current Permissions:"
echo "Long listing shows permissions:"
ls -l test_file.txt test_directory/
echo

echo "Permission breakdown for test_file.txt:"
ls -l test_file.txt | while read -r perms links owner group size month day time name; do
    echo "  Full permissions: $perms"
    echo "  File type: ${perms:0:1} (- = regular file, d = directory)"
    echo "  Owner permissions: ${perms:1:3}"
    echo "  Group permissions: ${perms:4:3}"
    echo "  Others permissions: ${perms:7:3}"
    echo "  Owner: $owner"
    echo "  Group: $group"
done
echo

echo "2. Changing Permissions with Symbolic Notation:"
echo "Add execute permission for owner:"
chmod u+x test_file.txt
ls -l test_file.txt

echo "Remove write permission for group:"
chmod g-w test_file.txt
ls -l test_file.txt

echo "Add read permission for others:"
chmod o+r test_file.txt
ls -l test_file.txt
echo

echo "3. Changing Permissions with Octal Notation:"
echo "Set permissions to 755 (rwxr-xr-x):"
chmod 755 test_file.txt
ls -l test_file.txt

echo "Set permissions to 644 (rw-r--r--):"
chmod 644 test_file.txt
ls -l test_file.txt

echo "Set permissions to 600 (rw-------):"
chmod 600 test_file.txt
ls -l test_file.txt
echo

echo "4. Directory Permissions:"
echo "Original directory permissions:"
ls -ld test_directory/

echo "Set directory permissions to 755:"
chmod 755 test_directory/
ls -ld test_directory/

echo "Set directory permissions to 700:"
chmod 700 test_directory/
ls -ld test_directory/
echo

echo "5. Common Permission Patterns:"
echo "Creating files with different permissions:"

# Create examples
touch readonly_file.txt
chmod 444 readonly_file.txt
echo "Read-only file (444):"
ls -l readonly_file.txt

touch executable_script.sh
echo '#!/bin/bash\necho "Hello World"' > executable_script.sh
chmod 755 executable_script.sh
echo "Executable script (755):"
ls -l executable_script.sh

touch private_file.txt
chmod 600 private_file.txt
echo "Private file (600):"
ls -l private_file.txt
echo

echo "6. Testing Permissions:"
echo "Testing read permission on readonly_file.txt:"
if [ -r readonly_file.txt ]; then
    echo "✓ File is readable"
    cat readonly_file.txt 2>/dev/null || echo "Content: (empty)"
else
    echo "✗ File is not readable"
fi

echo "Testing write permission on readonly_file.txt:"
if [ -w readonly_file.txt ]; then
    echo "✓ File is writable"
else
    echo "✗ File is not writable"
fi

echo "Testing execute permission on executable_script.sh:"
if [ -x executable_script.sh ]; then
    echo "✓ File is executable"
    echo "Running script:"
    ./executable_script.sh
else
    echo "✗ File is not executable"
fi
echo

echo "7. Umask Demo:"
echo "Current umask value:"
umask

echo "Creating file with current umask:"
touch umask_test.txt
ls -l umask_test.txt

echo "Setting umask to 022:"
umask 022
touch umask_022.txt
ls -l umask_022.txt

echo "Setting umask to 077:"
umask 077
touch umask_077.txt
ls -l umask_077.txt
echo

echo "8. File Permission Summary:"
echo "All test files with their permissions:"
ls -l *test*.txt *.sh 2>/dev/null | grep -E '\.(txt|sh)$'
echo

echo "=== File Permissions Demo Complete ==="
