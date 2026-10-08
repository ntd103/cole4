#!/bin/bash
# Demo script for Pipes and Filters section

echo "=== Pipes and Filters Demo ==="
echo

# Setup demo environment
cd /demo/data || exit 1

# Create sample data files for demonstration
echo "Creating sample data files..."
cat > employees.txt << EOF
John Doe,Engineering,85000,Manager
Jane Smith,Marketing,65000,Analyst
Bob Johnson,Engineering,75000,Developer
Alice Brown,HR,55000,Coordinator
Charlie Wilson,Marketing,70000,Manager
Diana Lee,Engineering,90000,Senior Developer
Eve Davis,HR,60000,Manager
Frank Miller,Engineering,80000,Developer
Grace Taylor,Marketing,62000,Analyst
Henry Clark,HR,58000,Coordinator
EOF

cat > numbers.txt << EOF
15
8
23
4
42
16
11
35
7
29
EOF

cat > server.log << EOF
2024-01-15 10:30:15 INFO User login: john_doe
2024-01-15 10:31:22 ERROR Database connection failed
2024-01-15 10:32:45 INFO User login: jane_smith
2024-01-15 10:35:10 WARNING High memory usage detected
2024-01-15 10:36:33 INFO User logout: john_doe
2024-01-15 10:38:47 ERROR File not found: /tmp/config.txt
2024-01-15 10:40:12 INFO User login: bob_johnson
2024-01-15 10:42:28 WARNING Disk space low
2024-01-15 10:45:55 ERROR Network timeout
2024-01-15 10:47:16 INFO System backup completed
EOF

echo "Sample data created."
echo

echo "1. Basic Pipe Usage:"
echo "Count lines in employees file:"
cat employees.txt | wc -l

echo "List files and search for .txt files:"
ls -la | grep ".txt"

echo "Sort numbers and display:"
cat numbers.txt | sort -n
echo

echo "2. grep - Pattern Searching:"
echo "Search for 'Engineering' in employees:"
grep "Engineering" employees.txt

echo "Case insensitive search for 'manager':"
grep -i "manager" employees.txt

echo "Show line numbers for errors in log:"
grep -n "ERROR" server.log

echo "Invert match - show non-ERROR lines:"
grep -v "ERROR" server.log | head -5
echo

echo "3. sort - Sorting Data:"
echo "Sort employees by name (first column):"
sort employees.txt

echo "Sort numbers in reverse order:"
sort -nr numbers.txt

echo "Sort employees by salary (3rd field, numeric):"
sort -t, -k3 -n employees.txt
echo

echo "4. uniq - Remove Duplicates:"
echo "Create file with duplicates:"
cat > duplicates.txt << EOF
apple
banana
apple
orange
banana
apple
grape
EOF

echo "Remove consecutive duplicates:"
uniq duplicates.txt

echo "Sort first, then remove duplicates:"
sort duplicates.txt | uniq

echo "Count occurrences:"
sort duplicates.txt | uniq -c
echo

echo "5. cut - Extract Columns:"
echo "Extract just names (first column):"
cut -d, -f1 employees.txt

echo "Extract department and salary:"
cut -d, -f2,3 employees.txt

echo "Extract first 10 characters of each line:"
cut -c 1-10 employees.txt
echo

echo "6. awk - Pattern Processing:"
echo "Print names and salaries with formatting:"
awk -F, '{printf "%-15s $%s\n", $1, $3}' employees.txt

echo "Calculate total salary:"
awk -F, '{sum += $3} END {printf "Total salary: $%d\n", sum}' employees.txt

echo "Find employees with salary > 70000:"
awk -F, '$3 > 70000 {print $1, $3}' employees.txt
echo

echo "7. sed - Stream Editor:"
echo "Replace 'Engineering' with 'Tech':"
sed 's/Engineering/Tech/' employees.txt | head -3

echo "Delete lines containing 'HR':"
sed '/HR/d' employees.txt

echo "Print only lines 2-4:"
sed -n '2,4p' employees.txt
echo

echo "8. Complex Pipeline Examples:"
echo "Top 3 highest paid employees:"
awk -F, '{print $3, $1}' employees.txt | sort -nr | head -3

echo "Count employees by department:"
cut -d, -f2 employees.txt | sort | uniq -c

echo "Find unique error types in log:"
grep "ERROR" server.log | awk '{print $4}' | sort | uniq

echo "Find average salary by department:"
awk -F, '
{
    dept[$2] += $3
    count[$2]++
}
END {
    for (d in dept) {
        printf "%-12s: $%.0f\n", d, dept[d]/count[d]
    }
}' employees.txt
echo

echo "9. Real-world Log Analysis:"
echo "Log file analysis:"
echo "Total log entries: $(wc -l < server.log)"
echo "Error count: $(grep -c "ERROR" server.log)"
echo "Warning count: $(grep -c "WARNING" server.log)"
echo "Info count: $(grep -c "INFO" server.log)"

echo "Most recent errors:"
grep "ERROR" server.log | tail -2

echo "Users who logged in:"
grep "User login" server.log | awk '{print $5}' | sort | uniq
echo

echo "10. Performance Monitoring Pipeline:"
echo "Simulating process monitoring:"
ps aux | head -1  # Header
ps aux | grep -v grep | sort -k3 -nr | head -5  # Top 5 CPU users
echo

echo "=== Pipes and Filters Demo Complete ==="
