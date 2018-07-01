#!/bin/sh
set -e

mkdir -p logs
broker/start.sh > logs/broker.log 2>&1;
scheduler/start.sh > logs/scheduler.log 2>&1;
visualizations/start.sh > logs/visualizations.log 2>&1;
nohup database_link/start.sh > /dev/null 2>&1 &

