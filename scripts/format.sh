#!/bin/bash

set -e

isort --recursive --force-single-line-imports app tests
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app tests
black app tests
isort --recursive app tests