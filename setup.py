from distutils.core import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
from setuptools.command.develop import develop

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='ESXi-Backup',
    version='0.1.2',
    author="Gabriel Melillo",
    author_email="gabriel@melillo.me",
    maintainer="Gabriel Melillo",
    maintainer_email="gabriel@melillo.me",
    description="Export configuration from ESXi 5.X host and upload it to a central repository",
    url="https://github.com/gmelillo/esxi-backup",
    install_requires=[
        "argparse==1.4.0",
        "easywebdav==1.2.0",
        "ecdsa==0.13.2",
        "paramiko==2.4.2",
        "pycryptodome==3.6.6",
        "requests==2.22.0",
        "wsgiref==0.1.2"
    ],
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    data_files=[
        ('esxi-backup', ['requirements.txt']),
        ('esxi-backup', ['esxi.ini.sample'])
    ],
    include_package_data=True,
    packages=[
        'esxibackup',
    ],
    license="GNU GENERAL PUBLIC LICENSE",
    long_description='Export configuration from ESXi 5.X host and upload it to a central repository'
                     '\n\n',
    entry_points = {'console_scripts': 'esxi-backup = esxibackup:main'}
)
