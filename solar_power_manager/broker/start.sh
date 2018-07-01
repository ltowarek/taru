#!/bin/sh
set -e
echo "Starting broker"
sudo systemctl start mosquitto
echo "Broker started"

