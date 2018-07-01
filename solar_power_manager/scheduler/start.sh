#!/bin/sh
set -e
echo "Starting scheduler"
BASEDIR=$(cd `dirname $0` && pwd)
CMD="* * * * * ${BASEDIR}/run.sh"
crontab -l > ${BASEDIR}/current_cron
grep -ve "$CMD" ${BASEDIR}/current_cron > ${BASEDIR}/new_cron || true
echo "${CMD}" >> ${BASEDIR}/new_cron
crontab ${BASEDIR}/new_cron
rm ${BASEDIR}/current_cron ${BASEDIR}/new_cron
echo "Scheduler started"

