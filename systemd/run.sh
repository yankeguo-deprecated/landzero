#!/bin/bash

COMMAND="${1}"

if [ -z "${COMMAND}" ]; then
    COMMAND=""
fi

set -eu

cd $(dirname $0)/..

source venv/bin/activate

case "${COMMAND}" in
    server)
        exec gunicorn -w 4 landzero.wsgi:application
        ;;
    celery-beat)
        exec celery -A landzero beat -l info
        ;;
    celery-worker)
        exec celery -A landzero worker -l info
        ;;
    *)
        echo "unknown command: ${COMMAND}"
        echo "usage: $0 {server|celery-beat|celery-worker}"
        exit 1
        ;;
esac
