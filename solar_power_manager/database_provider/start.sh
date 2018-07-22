#!/bin/sh
set -ex
echo "Starting database provider"
BASEDIR=$(cd `dirname $0` && pwd)
sudo systemctl start influxdb
sleep 10s
. $BASEDIR/../venv/bin/activate
python $BASEDIR/../arinna/database_provider.py
deactivate
echo "Database provider started"

