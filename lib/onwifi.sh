#!/bin/bash

# 1. get into the git repository
cd ~/Downloads/whiteboard_pi
git checkout raspberrypi
git pull origin raspberrypi

# 2. get the IP address into the ip.md file
hostname -I > ~/Downloads/whiteboard_pi/ip.md

# 3. push to the git repository
git add -A
git commit -m "AUTO: RasPi IP address [$(date)]"
git push origin raspberrypi
sudo systemctl status onwifi.service
