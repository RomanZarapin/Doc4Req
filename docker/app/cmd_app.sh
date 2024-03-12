#!/bin/bash

set -Eeuo pipefail

if [ $TASK_SLOT -eq 1 ]; then
    alembic upgrade head
fi

gunicorn -c ./config/gunicorn.py  main:app \
    >> /dev/stdout \
    2>> /dev/stdout
