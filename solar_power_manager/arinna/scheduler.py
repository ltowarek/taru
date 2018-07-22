#!/usr/bin/env python3

import crontab
import logging
import os
import sys


logger = logging.getLogger(__name__)


def setup_logging():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('scheduler.log')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def main():
    setup_logging()

    logger.info('Getting crontab')
    cron = crontab.CronTab(user=True)
    logger.debug('Current crontab: {}'.format(cron))

    script_directory = os.path.dirname(os.path.abspath(__file__))
    command = os.path.join(script_directory, '../publisher/run.sh')
    logger.info('Command: {}'.format(command))

    for _ in cron.find_command(command):
        logger.info('Job already exists')
    else:
        logger.info('Job not found')
        logger.info('Creating new job')
        job = cron.new(command=command)
        job.minute.every(1)
        logger.info('Job: {}'.format(job))
        cron.write()
        logger.info('New job created')

    return 0


if __name__ == '__main__':
    sys.exit(main())
