#!/bin/bash
# Setup script to make all demo scripts executable

echo "Setting up Unix/Linux Demo Environment..."
echo "Making all demo scripts executable..."

# Make all scripts executable
chmod +x demo-scripts/*.sh

echo "Demo scripts are now executable:"
ls -la demo-scripts/*.sh | awk '{print $1, $9}'

echo
echo "Setup complete! You can now:"
echo "1. Start the environment: docker-compose up -d"
echo "2. Enter the main container: docker exec -it unix-linux-demo bash"
echo "3. Run demos: cd /demo && bash scripts/master-demo.sh"
echo
echo "For detailed instructions, see DEMO-GUIDE.md"
