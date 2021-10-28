# npmrd_curator

Backend + Frontend for NP-MRD curator applet.

## DB

This app runs on a small database. You will need to modify the `api` service in `docker-compose.yml`
to either point to a file based sqlite database (persisted through a shared file mount in docker),
or configure the `POSTGRES_URI` environment variable (REMOVE this variable if you are not using an
external database or the app will fail to launch due to a psql connection error).

## Production docker-compose

To run this app in a production environment, you can simply copy the `docker-compose.yml` file
and modify as needed. If you have access to the `ghcr.io/liningtonlab` GitHub container registry,
then you can simply `docker-compose pull` to get the latest images. Otherwise, modify the `docker-build-push.sh`
file to build the images locally and push to your desired container registry and then
`docker-compose.yml` accordingly. You can also modify the labels in `docker-compose.yml` to work with
the [Traefik reverse proxy](https://doc.traefik.io/traefik/).

To launch the stack:

```bash
docker-compose up -d
```

## Running locally

There are two separate components that will eventually get composed into Docker containers:

1. Backend

Python backend uses FastAPI, which should be run using uvicorn:

```bash
uvicorn main:app --reload
```

2. Frontend

JavaScript frontend uses NuxtJS (Vue.js) and should be run using yarn:

```
cd npmrd_curator_app
yarn dev
```

## Dependencies

The below assumes that you have both [Anaconda Python](https://www.anaconda.com/products/individual), and [yarn](https://yarnpkg.com/) installed and available to you.

```bash
conda env create -f environment.yml
```

```bash
cd npmrd_curator_app
yarn
```

Dev dependencies can also be installed with

`pip install -r dev-requirements.txt`

## Testing

Python tests can be run using the `pytest` framework.
