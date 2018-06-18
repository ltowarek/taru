#!/bin/sh
sudo systemctl start influxdb
python database_link.py

