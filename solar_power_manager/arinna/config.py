#!/usr/bin/env python3

import os


def get_root_directory():
    default_path = os.path.abspath(os.path.join(__file__, '..'))
    return os.environ.get('ARINNA_ROOT', default_path)


def get_logs_directory():
    return os.path.join(get_root_directory(), 'logs')


def get_log_path(file_name):
    return os.path.join(get_logs_directory(), file_name + '.log')
