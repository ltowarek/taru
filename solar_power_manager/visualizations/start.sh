#!/bin/sh
set -ex
echo "Starting visualtizations"
sudo systemctl start grafana-server
echo "Visualizations started"

