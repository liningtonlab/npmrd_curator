FROM jvansan/uvicorn-gunicorn:3.9

LABEL Name=npmrd_curator_api Version=0.1.1

ENV PYTHONVENV=app
RUN conda install -n $PYTHONVENV -c conda-forge fastapi rdkit \
    pydantic pandas sqlalchemy beautifulsoup4 lxml jinja2 psycopg2

COPY ./npmrd_curator /app/npmrd_curator
ENV MODULE_NAME=npmrd_curator.main