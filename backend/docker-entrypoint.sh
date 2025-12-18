#!/bin/bash

# 1. Export environment variables to a file so cron can read them
# We filter out some internal system vars to avoid conflicts
printenv | grep -v "no_proxy" >> /etc/environment

# Create a shell script that exports these for easy sourcing in cron
printenv | sed 's/^\(.*\)$/export \1/g' > /app/env.sh
chmod +x /app/env.sh

# 2. Install the crontab
crontab /app/crontab/cron_scheduler

# 3. Start cron in the background
cron

# 4. Start the Gunicorn app
exec gunicorn -k uvicorn.workers.UvicornWorker -c /app/gunicorn_conf.py npmrd_curator.main:app