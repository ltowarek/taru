#!/bin/sh
set -e

nohup ./broker/start.sh </dev/null > logs/broker.log 2>&1 &
nohup ./database_link/start.sh </dev/null > logs/database_link.log 2>&1 &
nohup ./scheduler/start.sh </dev/null > logs/scheduler.log 2>&1 &
nohup ./visualizations/start.sh >/dev/null > logs/visualizations.log 2>&1 &

