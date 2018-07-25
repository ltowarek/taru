#!/usr/bin/env python3

import argparse
import crontab
import logging
import logging.handlers
import os
import sys
import arinna.config as config


logger = logging.getLogger(__name__)


def get_command_line():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_directory, '../scripts/publish.sh')


def register():
    logger.info('Getting crontab')
    cron = crontab.CronTab(user=True)
    logger.debug('Current crontab: {}'.format(cron))

    command = get_command_line()
    logger.info('Command: {}'.format(command))

    if list(cron.find_command(command)):
        logger.info('Job already exists')
    else:
        logger.info('Job not found')
        logger.info('Creating new job')
        job = cron.new(command=command)
        job.minute.every(1)
        logger.info('Job: {}'.format(job))
        cron.write()
        logger.info('New job created')


def unregister():
    logger.info('Getting crontab')
    cron = crontab.CronTab(user=True)
    logger.debug('Current crontab: {}'.format(cron))

    command = get_command_line()
    logger.info('Command: {}'.format(command))

    existing_jobs = list(cron.find_command(command))
    if not existing_jobs:
        logger.info('Job not found')
    else:
        logger.info('Job found')
        logger.info('Removing job')
        logger.info('Job: {}'.format(existing_jobs))
        cron.remove(existing_jobs)
        cron.write()
        logger.info('Job removed')


def setup_logging():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.handlers.RotatingFileHandler(config.get_log_path('scheduler'),
                                                        maxBytes=1000 * 1000, backupCount=1)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


actions = {
    'register': register,
    'unregister': unregister
}


def process_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=actions.keys())
    return parser.parse_args()


def main():
    args = process_command_line()
    setup_logging()
    actions[args.action]()
    return 0


if __name__ == '__main__':
    sys.exit(main())
