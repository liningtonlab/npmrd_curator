FROM python:3.9

WORKDIR /app/

LABEL Name=npmrd_curator_api Version=0.1.1

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv lock -r > requirements.txt && pip install -r requirements.txt

COPY ./gunicorn_conf.py ./gunicorn_conf.py

COPY ./npmrd_curator ./npmrd_curator

EXPOSE 80

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/app/gunicorn_conf.py", "npmrd_curator.main"]