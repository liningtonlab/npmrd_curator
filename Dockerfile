FROM jvansan/uvicorn-gunicorn:3.7

LABEL Name=npmrd_curator_api Version=0.1.0

ENV PYTHONVENV=app
RUN conda install -n $PYTHONVENV -c conda-forge fastapi

COPY ./npmrd_curator /app/app

# CMD ["/start-reload.sh"]