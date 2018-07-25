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

        logger.info('Registering scheduler')
        self.processes.append(self.run_process(
            'python {} register'.format(os.path.normpath(os.path.join(root_directory, 'arinna/scheduler.py'))),
        ))
        logger.info('Scheduler registered')

    def run_process(self, command):
        logger.debug('Command: {}'.format(command))
        process = subprocess.Popen('exec {}'.format(command), shell=True)
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

        logger.info('Unregistering scheduler')
        root_directory = config.get_root_directory()
        self.processes.append(self.run_process(
            'python {} unregister'.format(os.path.normpath(os.path.join(root_directory, 'arinna/scheduler.py'))),
        ))
        logger.info('Scheduler unregistered')


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
    signal.signal(signal.SIGTERM, app.stop)
    app.start()
    app.wait()
    return 0


sys.exit(main())
