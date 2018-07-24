#!/usr/bin/env python3

import logging
import os
import signal
import subprocess
import sys
import arinna.config as config


logger = logging.getLogger(__name__)


class ArinnaApplication:
    def __init__(self):
        self.processes = []
        signal.signal(signal.SIGTERM, self.stop)

    def start(self):
        root_directory = config.get_root_directory()

        logger.info('Starting database provider')
        self.processes.append(self.run_process(
            'python {}'.format(os.path.normpath(os.path.join(root_directory, 'arinna/database_provider.py'))),
        ))
        logger.info('Database provider started')

        logger.info('Starting inverter provider')
        self.processes.append(self.run_process(
            'python {}'.format(os.path.normpath(os.path.join(root_directory, 'arinna/inverter_provider.py'))),
        ))
        logger.info('Inverter provider started')

        logger.info('Starting scheduler')
        self.processes.append(self.run_process(
            'python {}'.format(os.path.normpath(os.path.join(root_directory, 'arinna/scheduler.py'))),
        ))
        logger.info('Scheduler started')

    def run_process(self, command):
        logger.debug('Command: {}'.format(command))
        process = subprocess.Popen(command, shell=True)
        logger.debug('PID: {}'.format(process.pid))
        return process

    def wait(self):
        logger.info('Waiting for processes')
        try:
            for p in self.processes:
                p.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
        logger.info('Processes exited')

    def stop(self, signum=None, frame=None):
        logger.info('Stopping processes')
        for p in self.processes:
            p.terminate()
        logger.info('Processes stopped')


def setup_logging():
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def main():
    setup_logging()
    app = ArinnaApplication()
    app.start()
    app.wait()
    return 0


sys.exit(main())
