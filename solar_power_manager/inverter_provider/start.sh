#!/bin/sh
set -ex
echo "Starting inverter provider"
BASEDIR=$(cd `dirname $0` && pwd)
. $BASEDIR/../venv/bin/activate
python $BASEDIR/../arinna/inverter_provider.py
deactivate
echo "Inverter provider started"
