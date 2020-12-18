FROM jvansan/uvicorn-gunicorn:3.7

LABEL Name=npmrd_curator_api Version=0.1.0

ENV PYTHONVENV=curator
COPY environment.yml /app
RUN conda env create -f environment.yml
RUN conda install -n $PYTHONVENV -c conda-forge gunicorn

COPY ./npmrd_curator /app/npmrd_curator
ENV MODULE_NAME=npmrd_curator.main
# CMD ["/start-reload.sh"]