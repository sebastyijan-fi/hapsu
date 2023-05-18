#!/bin/bash

set -x

echo "Starting setup..."

echo "Installing pip..."
sudo apt update && sudo apt install python3-pip -y || { echo "pip installation failed"; exit 1; }

echo "Installing Node.js and npm..."
sudo apt install nodejs npm -y || { echo "Node.js/npm installation failed"; exit 1; }

echo "Installing PM2..."
sudo npm install pm2 -g || { echo "PM2 installation failed"; exit 1; }

# Check if the directory for the repo exists
if [ ! -d "/hapsu" ]; then
    echo "Cloning the repo..."
    sudo git clone https://github.com/sebastyijan-fi/hapsu.git /hapsu || { echo "Git clone failed"; exit 1; }
fi

# Navigate to the repo directory
cd /hapsu || { echo "Could not navigate to repo directory"; exit 1; }

# Check if the .env file exists
if [ ! -f ".env" ]; then
    # Copy env.txt to .env
    sudo cp env.txt .env
    echo "Please enter your tokens in the .env file"
    # Ask the user if they want to change the .env keys
    read -p "Do you want to change .env keys now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        sudo nano .env
    fi
else
    # Ask the user if they want to change the .env keys
    read -p "Do you want to change .env keys? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        sudo nano .env
    fi
fi

echo "Installing Python packages..."
sudo pip install -r requirements.txt || { echo "Package installation failed"; exit 1; }

echo "Starting the bot with PM2..."
sudo   pm2 start bot.py --name hapsu --interpreter python3 || { echo "PM2 start failed"; exit 1; }

echo "Saving the PM2 process list..."
sudo pm2 save || { echo "PM2 save failed"; exit 1; }

echo "Setting up cron jobs..."

# Pull updates from git every 3 days at 12:00 AM
(crontab -l ; echo "0 0 */3 * * cd /hapsu && git pull && sudo pm2 restart hapsu") | crontab -

# This will update and upgrade the server every day at 12:00 AM
(crontab -l ; echo "0 0 * * * apt-get update && apt-get upgrade -y") | crontab -

echo "Setup complete!"
