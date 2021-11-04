# npmrd_curator

Backend + Frontend for NP-MRD curator applet.

## TODO

- Instructions for getting submission data from DB

## DB

This app runs on a small database. You will need to modify the `api` service in `docker-compose.yml`
to either point to a file based sqlite database (persisted through a shared file mount in docker),
or configure the `POSTGRES_URI` environment variable (REMOVE this variable if you are not using an
external database or the app will fail to launch due to a psql connection error).

The app (via SQLAlchemy) should automatically handle setting up the necessary tables. It will not however
create a postgres database for you (it must be able to connect).

## Production docker-compose

**TODO** replace with AWS copilot instructions.

~~To run this app in a production environment, you can simply copy the `docker-compose.yml` file
and modify as needed. If you have access to the `ghcr.io/liningtonlab` GitHub container registry,
then you can simply `docker-compose pull` to get the latest images. Otherwise, modify the `docker-build-push.sh`
file to build the images locally and push to your desired container registry and then
`docker-compose.yml` accordingly. You can also modify the labels in `docker-compose.yml` to work with
the [Traefik reverse proxy](https://doc.traefik.io/traefik/).~~

To launch the stack:

```bash
docker-compose up -d
```

## Running locally

### Docker-compose development

Modify the `docker-compose.yml` to suite your needs for a database. By default I recommend using the SQLite
DB for development. Then launching the app for development is as simple as

```bash
docker-compose up -d

# OPTIONAL: Check the logs of api
docker-compose logs -f api
# OPTIONAL: Check the logs of app
docker-compose logs -f app
```

### Local installs

There are two separate components that are also composed into Docker containers:

### 1. Backend

Python backend uses FastAPI, which should be run using uvicorn:

```bash
cd backend
uvicorn npmrd_curator.main:app --reload
```

### 2. Frontend

JavaScript frontend uses NuxtJS (Vue.js) and should be run using yarn:

```bash
cd frontend
yarn dev
```

## Dependencies

The below assumes that you have both [pipenv](https://pypi.org/project/pipenv/), and [yarn](https://yarnpkg.com/)
installed and available to you. Note the `pipenv` install may fail on Windows due to the
[`rdkit-pypi`](https://pypi.org/project/rdkit-pypi/) package (This is untested).

```bash
cd backend
pipenv install --dev
```

```bash
cd frontend
yarn
```

## Testing

Python tests can be run using the `pytest` framework.
