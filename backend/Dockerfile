FROM python:3.9

WORKDIR /app/

LABEL Name=npmrd_curator_api Version=0.1.2

# Install vim and cron
RUN apt-get update && apt-get install -y vim cron && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn

# Setup logs directory
RUN mkdir -p /app/logs

# Copy files
COPY ./gunicorn_conf.py ./gunicorn_conf.py
COPY ./npmrd_curator ./npmrd_curator
COPY ./json_extraction_scripts ./json_extraction_scripts
COPY ./crontab ./crontab

# Copy entrypoint script
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose port for the app
EXPOSE 80
ENV WEB_CONCURRENCY 1

# Setup directory for sqlite if needed
RUN mkdir -p db

# Start cron and the FastAPI app via entrypoint
CMD ["/docker-entrypoint.sh"]
