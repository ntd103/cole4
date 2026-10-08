#!/bin/bash
# Demo script for Process Management section

echo "=== Process Management Demo ==="
echo

echo "1. Viewing Processes:"
echo "Show all processes (first 10):"
ps aux | head -10

echo "Show processes in tree format:"
if command -v pstree &> /dev/null; then
    pstree | head -10
else
    echo "pstree not available, using ps with hierarchy:"
    ps auxf | head -10
fi
echo

echo "2. Process Information:"
echo "Current shell process:"
ps aux | grep $$ | grep -v grep

echo "Process details for current shell:"
echo "PID: $$"
echo "Parent PID: $PPID"
echo "Process group: $(ps -o pgid= -p $$)"
echo

echo "3. Starting Background Processes:"
echo "Starting a long-running process in background:"
sleep 30 &
bg_pid=$!
echo "Background process PID: $bg_pid"

echo "Starting another background process:"
(for i in {1..20}; do echo "Counter: $i"; sleep 2; done) &
counter_pid=$!
echo "Counter process PID: $counter_pid"

echo "List current jobs:"
jobs
echo

echo "4. Process Control:"
echo "Checking if background processes are running:"
if kill -0 $bg_pid 2>/dev/null; then
    echo "Sleep process (PID: $bg_pid) is still running"
else
    echo "Sleep process (PID: $bg_pid) has finished"
fi

if kill -0 $counter_pid 2>/dev/null; then
    echo "Counter process (PID: $counter_pid) is still running"
else
    echo "Counter process (PID: $counter_pid) has finished"
fi
echo

echo "5. Process Priorities:"
echo "Starting processes with different nice values:"
nice -n 10 sleep 5 &
nice_pid=$!
echo "Started process with nice value 10, PID: $nice_pid"

echo "Process priority information:"
ps -o pid,ppid,ni,cmd -p $nice_pid 2>/dev/null || echo "Process may have finished"
echo

echo "6. System Monitoring:"
echo "System load average:"
uptime

echo "Memory usage:"
free -h 2>/dev/null || echo "free command not available"

echo "Disk usage:"
df -h / 2>/dev/null | grep -v "Filesystem"

echo "Top processes by CPU (using ps):"
ps aux --sort=-%cpu | head -6
echo

echo "7. Process Lifecycle Demo:"
echo "Creating a process and monitoring its lifecycle:"

# Create a test script
cat > /tmp/test_process.sh << 'EOF'
#!/bin/bash
echo "Process started: PID $$"
for i in {1..10}; do
    echo "Working... step $i"
    sleep 1
done
echo "Process completed: PID $$"
EOF

chmod +x /tmp/test_process.sh

echo "Starting test process:"
/tmp/test_process.sh &
test_pid=$!
echo "Test process PID: $test_pid"

echo "Monitoring process status:"
sleep 2
if kill -0 $test_pid 2>/dev/null; then
    echo "Process $test_pid is running"
    ps -o pid,ppid,stat,time,cmd -p $test_pid
fi

echo "Waiting for process to complete..."
wait $test_pid
echo "Process $test_pid exit status: $?"
echo

echo "8. Signal Handling Demo:"
echo "Creating a signal-handling process:"

cat > /tmp/signal_demo.sh << 'EOF'
#!/bin/bash
cleanup() {
    echo "Received signal, cleaning up..."
    exit 0
}

trap cleanup SIGTERM SIGINT

echo "Signal demo process started: PID $$"
while true; do
    echo "Running... (send SIGTERM to stop gracefully)"
    sleep 3
done
EOF

chmod +x /tmp/signal_demo.sh

echo "Starting signal demo process:"
/tmp/signal_demo.sh &
signal_pid=$!
echo "Signal demo PID: $signal_pid"

sleep 5
echo "Sending SIGTERM to process $signal_pid:"
kill -TERM $signal_pid

wait $signal_pid 2>/dev/null
echo "Signal demo process terminated"
echo

echo "9. Job Control Examples:"
echo "Current active jobs:"
jobs

echo "Bringing a job to foreground (if any):"
# This is just for demonstration - in interactive shell you'd use fg

echo "Terminating remaining background processes:"
for pid in $bg_pid $counter_pid; do
    if kill -0 $pid 2>/dev/null; then
        echo "Terminating process $pid"
        kill $pid
    fi
done

# Wait a moment for processes to terminate
sleep 2

echo "Final job status:"
jobs
echo

echo "10. Process Monitoring Script:"
cat > /tmp/monitor.sh << 'EOF'
#!/bin/bash
echo "=== System Process Monitor ==="
echo "Timestamp: $(date)"
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}' 2>/dev/null || echo "N/A")"
echo "Process Count: $(ps aux | wc -l)"
echo "Top 3 CPU Processes:"
ps aux --sort=-%cpu | head -4 | tail -3
echo "================================"
EOF

chmod +x /tmp/monitor.sh
echo "Running system monitor:"
/tmp/monitor.sh
echo

echo "=== Process Management Demo Complete ==="

# Cleanup
rm -f /tmp/test_process.sh /tmp/signal_demo.sh /tmp/monitor.sh
