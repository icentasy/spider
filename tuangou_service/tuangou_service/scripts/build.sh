#!/bin/bash
#
# This scripts is used to build the application.
#
#
# Author : chzhong
#

python setup.py -q build
python setup.py -q sdist
