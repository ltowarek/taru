#!/bin/sh
set -e
echo "Starting database link"
BASEDIR=$(cd `dirname $0` && pwd)
sudo systemctl start influxdb
sleep 10s
. $BASEDIR/../venv/bin/activate
python $BASEDIR/database_link.py
deactivate
echo "Database link started"

