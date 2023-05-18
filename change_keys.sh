#!/bin/bash

set -x

echo "Starting key setup..."

# Navigate to the repo directory
cd /hapsu || { echo "Could not navigate to repo directory"; exit 1; }

# Check if the .env file exists
if [ ! -f ".env" ]; then
    # If it doesn't exist, create one by copying from env.txt
    sudo cp env.txt .env
    echo "Please enter your tokens in the .env file"
fi

# Ask the user if they want to change the .env keys
read -p "Do you want to change .env keys now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo nano .env
fi

echo "Key setup complete!"
