#!/bin/sh
set -e
BASEDIR=$(cd `dirname $0` && pwd)
CMD="* * * * * ${BASEDIR}/run.sh"
crontab -l > current_cron
grep -ve "$CMD" current_cron > new_cron
crontab new_cron
rm current_cron new_cron

