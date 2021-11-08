FROM python:3.9

WORKDIR /app/

LABEL Name=npmrd_curator_api Version=0.1.1

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv lock -r > requirements.txt && pip install -r requirements.txt && pip install gunicorn

COPY ./gunicorn_conf.py ./gunicorn_conf.py

COPY ./npmrd_curator ./npmrd_curator

EXPOSE 80
ENV WEB_CONCURRENCY 1
# setup directory for sqlite if needed
RUN ["mkdir", "db"]

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/app/gunicorn_conf.py", "npmrd_curator.main:app"]
