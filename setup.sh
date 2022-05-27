#!/bin/bash

# Update package list
sudo apt-get update
sudo apt-get -y upgrade

# Additional apt packages
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-venv -y
sudo apt-get install libatlas-base-dev -y # for numpy
sudo apt-get install libopenjp2-7 -y # for visuals

# Github Credentials
git config pull.rebase false

# Set up locale, timezone, language
sudo timedatectl set-timezone US/Central

# Virtual Environment Setup
rm -rf ~/bleed-orange-measure-iaq/.venv # remove if it already exists
mkdir ~/bleed-orange-measure-iaq/.venv
python3 -m venv ~/bleed-orange-measure-iaq/.venv

# Dashboard update script
sudo /bin/bash -c 'echo "*/15 * * * * pi sh /home/pi/bleed-orange-measure-iaq/udpate_figures.sh" >> /etc/crontab'
