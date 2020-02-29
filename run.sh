#!/bin/bash

set -eu

cd $(dirname $0)

source venv/bin/activate

exec gunicorn -w 4 landzero.wsgi:application