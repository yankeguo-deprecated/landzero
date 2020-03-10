#!/bin/bash

set -eu

cd $(dirname $0)
source venv/bin/activate

exec  celery -A landzero beat -l info
