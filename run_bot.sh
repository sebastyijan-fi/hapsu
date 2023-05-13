#!/bin/bash

echo "Starting setup..."

# Check if the directory for the repo exists
if [ ! -d "/hapsu" ]; then
    echo "Cloning the repo..."
    sudo git clone git@github.com:sebastyijan-fi/hapsu.git /hapsu || { echo "Git clone failed"; exit 1; }
fi

# Navigate to the repo directory
cd /hapsu || { echo "Could not navigate to repo directory"; exit 1; }

# Check if the .env file exists
if [ ! -f ".env" ]; then
    # Copy env.txt to .env
    sudo cp env.txt .env
    echo "Please enter your tokens in the .env file"
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
sudo pm2 start bot.py --name hapsu || { echo "PM2 start failed"; exit 1; }

echo "Saving the PM2 process list..."
sudo pm2 save || { echo "PM2 save failed"; exit 1; }

echo "Setting up cron jobs..."
(crontab -l ; echo "0 0 * * * cd /hapsu && git pull") | crontab -
(crontab -l ; echo "0 0 * * * apt-get update && apt-get upgrade -y") | crontab -

echo "Setup complete!"
