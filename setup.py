from distutils.core import setup
from pip.req import parse_requirements
from setuptools.command.develop import develop

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Information Technology',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().split("\n")

setup(
    name='ESXi-Backup',
    version='0.1.2',
    author="Gabriel Melillo",
    author_email="gabriel@melillo.me",
    maintainer="Gabriel Melillo",
    maintainer_email="gabriel@melillo.me",
    description="Export configuration from ESXi 5.X host and upload it to a central repository",
    url="https://github.com/gmelillo/esxi-backup",
    install_requires=REQUIREMENTS,
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
