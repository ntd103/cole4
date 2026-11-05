#!/bin/bash
# Demo script for Network Communication Utilities section

echo "=== Network Communication Utilities Demo ==="
echo

echo "1. Basic Network Commands:"
echo "Testing connectivity with ping:"
echo "Pinging Google DNS (limited to 3 packets):"
ping -c 3 8.8.8.8 || echo "Ping failed or not available"
echo

echo "Pinging web server container:"
ping -c 2 web-server 2>/dev/null || echo "Web server not reachable from this container"
echo

echo "2. Network Information Commands:"
echo "Show network interfaces:"
if command -v ifconfig &> /dev/null; then
    ifconfig | head -20
elif command -v ip &> /dev/null; then
    ip addr show | head -20
else
    echo "Network interface commands not available"
fi
echo

echo "3. Network Connections:"
echo "Show listening ports and connections:"
if command -v netstat &> /dev/null; then
    echo "Using netstat:"
    netstat -tuln | head -10
elif command -v ss &> /dev/null; then
    echo "Using ss (modern netstat):"
    ss -tuln | head -10
else
    echo "Network statistics commands not available"
fi
echo

echo "4. DNS Lookup Commands:"
echo "DNS lookup for google.com:"
if command -v nslookup &> /dev/null; then
    nslookup google.com | head -10
elif command -v dig &> /dev/null; then
    dig +short google.com
else
    echo "DNS lookup commands not available"
fi
echo

echo "5. File Download with wget:"
echo "Downloading a small test file:"
cd /demo/data
if command -v wget &> /dev/null; then
    echo "Using wget to download from web server:"
    wget -q --timeout=5 http://web-server/ -O downloaded_page.html 2>/dev/null && \
        echo "Downloaded $(wc -c < downloaded_page.html) bytes" || \
        echo "Download failed - web server may not be ready"
else
    echo "wget not available"
fi
echo

echo "6. File Download with curl:"
if command -v curl &> /dev/null; then
    echo "Using curl to download from web server:"
    curl -s --connect-timeout 5 http://web-server/ -o curl_page.html 2>/dev/null && \
        echo "Downloaded $(wc -c < curl_page.html) bytes" || \
        echo "Download failed - web server may not be ready"
    
    echo "Getting HTTP headers:"
    curl -I --connect-timeout 5 http://web-server/ 2>/dev/null || \
        echo "Could not get headers - web server may not be ready"
else
    echo "curl not available"
fi
echo

echo "7. Network Service Testing:"
echo "Testing if web server is responding:"
if command -v curl &> /dev/null; then
    if curl -s --connect-timeout 5 http://web-server/ > /dev/null 2>&1; then
        echo "✓ Web server is responding"
    else
        echo "✗ Web server is not responding"
    fi
fi

echo "Testing if database server is responding:"
if command -v nc &> /dev/null; then
    if nc -z db-server 3306 2>/dev/null; then
        echo "✓ Database server port 3306 is open"
    else
        echo "✗ Database server port 3306 is not accessible"
    fi
elif timeout 3 bash -c "</dev/tcp/db-server/3306" 2>/dev/null; then
    echo "✓ Database server port 3306 is open"
else
    echo "✗ Database server port 3306 is not accessible"
fi
echo

echo "8. Network Monitoring:"
echo "Show routing table:"
if command -v route &> /dev/null; then
    route -n | head -5
elif command -v ip &> /dev/null; then
    ip route | head -5
else
    echo "Routing commands not available"
fi
echo

echo "9. Simple HTTP Request Demo:"
echo "Making HTTP requests to different services:"

# Test local web server
echo "Testing web server:"
if command -v curl &> /dev/null; then
    response=$(curl -s --connect-timeout 5 -w "%{http_code}" http://web-server/ 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "HTTP Response Code: ${response: -3}"
    else
        echo "Connection failed"
    fi
fi

# Test external service
echo "Testing external service (httpbin.org):"
if command -v curl &> /dev/null; then
    curl -s --connect-timeout 5 http://httpbin.org/ip 2>/dev/null | head -3 || \
        echo "External service not reachable"
fi
echo

echo "10. Network File Transfer Simulation:"
echo "Simulating file transfer between containers:"

# Create a test file
echo "Creating test file for transfer:"
echo "This is a test file for network transfer demo" > test_transfer.txt
echo "Test file created: $(ls -lh test_transfer.txt)"

# Simulate SCP-like operation (using container volumes)
echo "Simulating secure copy to backup location:"
cp test_transfer.txt /demo/backup/
if [ -f /demo/backup/test_transfer.txt ]; then
    echo "✓ File successfully 'transferred' to backup location"
    ls -lh /demo/backup/test_transfer.txt
else
    echo "✗ File transfer failed"
fi
echo

echo "11. Port Scanning Demo:"
echo "Checking common ports on localhost:"
common_ports=(22 23 25 53 80 110 143 443 993 995)

for port in "${common_ports[@]}"; do
    if timeout 1 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
        echo "Port $port: OPEN"
    else
        echo "Port $port: CLOSED"
    fi
done
echo

echo "12. Network Configuration Summary:"
echo "Network interface summary:"
hostname -I 2>/dev/null || echo "Hostname command not available"

echo "Container hostname:"
hostname

echo "Container IP in demo network:"
hostname -i 2>/dev/null || ip route get 1 | awk '{print $NF;exit}' 2>/dev/null || echo "IP not available"
echo

echo "=== Network Communication Utilities Demo Complete ==="

# Cleanup
rm -f test_transfer.txt downloaded_page.html curl_page.html
