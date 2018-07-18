#!/bin/sh
set -ex
echo "Starting inverter link"
BASEDIR=$(cd `dirname $0` && pwd)
. $BASEDIR/../venv/bin/activate
python $BASEDIR/inverter_link.py
deactivate
echo "Inverter link started"

