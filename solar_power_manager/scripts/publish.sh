#!/bin/sh
set -e
BASEDIR=$(cd `dirname $0` && pwd)
PYTHONPATH=$BASEDIR/.. python $BASEDIR/../arinna/publisher.py
