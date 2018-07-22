#!/bin/sh
set -e
BASEDIR=$(cd `dirname $0` && pwd)
. $BASEDIR/../venv/bin/activate
python $BASEDIR/../arinna/publisher.py
deactivate
