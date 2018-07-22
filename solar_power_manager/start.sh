#!/bin/sh
set -ex

mkdir -p logs
broker/start.sh > logs/broker.log 2>&1;
publisher/start.sh > logs/publisher.log 2>&1;
visualizations/start.sh > logs/visualizations.log 2>&1;
nohup database_provider/start.sh > /dev/null 2>&1 &
nohup inverter_provider/start.sh > /dev/null 2>&1 &
