import setuptools

with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='arinna',
    author='Łukasz Towarek',
    author_email='lukasz.towarek@gmail.com',
    description='Solar power manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['arinna']),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux'
    ),
    use_scm_version={'root': '..', 'relative_to': __file__, 'write_to': 'solar_power_manager/arinna/version.py'},
    setup_requires=['setuptools_scm'],
    install_requires=[
        'paho-mqtt',
        'influxdb',
        'pyserial',
        'python-crontab',
        'pyyaml'
    ],
    extras_require={
        'dev': [
            'setuptools_scm'
        ]
    },
    url='https://github.com/ltowarek/taru',
    project_urls={
        'Bug Reports': 'https://github.com/ltowarek/taru/issues',
        'Source': 'https://github.com/ltowarek/taru',
    },
    entry_points={
        'console_scripts': [
            'arinna = arinna.__main__:main',
            'arinna-database = arinna.database_provider:main',
            'arinna-inverter = arinna.inverter_provider:main',
            'arinna-scheduler = arinna.scheduler:main',
            'arinna-publisher = arinna.publisher:main'
        ]
    }
)
