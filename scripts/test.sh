#!/bin/bash

set -e
set -x

pytest --cov=app --cov=tests --cov-report=term-missing --cov-config=setup.cfg --cov-report=xml --cov-fail-under=80 --numprocesses=auto ${@}