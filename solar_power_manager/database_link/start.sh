#!/bin/sh
set -e
sudo systemctl start influxdb
BASEDIR=$(cd `dirname $0` && pwd)
. $BASEDIR/../venv/bin/activate
python $BASEDIR/database_link.py
deactivate

