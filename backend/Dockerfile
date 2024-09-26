FROM python:3.9

WORKDIR /app/

LABEL Name=npmrd_curator_api Version=0.1.2

# Install vim and other dependencies
RUN apt-get update && apt-get install -y vim

# Install pipenv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn

COPY ./gunicorn_conf.py ./gunicorn_conf.py
COPY ./npmrd_curator ./npmrd_curator

EXPOSE 80
ENV WEB_CONCURRENCY 1

# Setup directory for sqlite if needed
RUN ["mkdir", "db"]

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/app/gunicorn_conf.py", "npmrd_curator.main:app"]
