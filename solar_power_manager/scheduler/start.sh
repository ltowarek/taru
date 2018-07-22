#!/bin/sh
set -ex
echo "Starting scheduler"
BASEDIR=$(cd `dirname $0` && pwd)
. $BASEDIR/../venv/bin/activate
python $BASEDIR/../arinna/scheduler.py
deactivate
echo "Scheduler started"
