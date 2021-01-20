#!/usr/bin/env sh

exec uvicorn --reload --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*" src.main:app
