#!/usr/bin/env sh

if [[ -z "${PHA_DEPLOY_MODE_PROD}" ]]; then
    exec uvicorn --reload --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*" src.main:app
elif [[ -z "${PHA_DEPLOY_MODE_DEV}" ]]; then
    exec gunicorn -k uvicorn.workers.UvicornWorker -w 2 src.main:app
else
    echo "Neither PHA_DEPLOY_MODE_PROD nor PHA_DEPLOY_MODE_DEV was set, so not running anything."
fi
