#!/bin/sh
set -ex
echo "Starting broker"
sudo systemctl start mosquitto
echo "Broker started"

