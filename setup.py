# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
import sys

# file read helper
def read_from_file(path):
    if os.path.exists(path):
        with open(path,"rb","utf-8") as input:
            return input.read()

version = "0.4.7"

setup(
    name='sadcat',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='A ssh config generator I dont recommend to use',
    long_description=read_from_file('README.rst'),

    # The project's main homepage.
    url='https://github.com/noqqe/sadcat',

    # Author details
    author='Florian Baumann',
    author_email='flo@noqqe.de',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='ssh config templating generator ssh_config toml',
    packages=find_packages(),
    zip_safe=True,

    # dependencies
    install_requires=['toml'],

    # extra_requires
    extras_require={
        'dev': [
            'versionbump',
            'gitchangelog'
        ]
    },

    entry_points={
        'console_scripts': [
            'sadcat=sadcat.sadcat:main',
        ],
    },
)
