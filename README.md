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

### Copilot initialization

AWS Copilot has been used to deploy this stack into an existing VPC so that we can connect to a central RDS instance.

Make sure to initialize backend before frontend or DNS rules will cause an issue...

Make sure you enable the security group AFTER the `copilot env init` step below.

Instructions are available [HERE](https://github.com/liningtonlab/deployment_wiki/wiki/AWS).

See deployment [wiki page on common docs.](https://github.com/liningtonlab/deployment_wiki/wiki/AWS).

While you can use the interactive copilot CLI for steps, these instructions will complete the necessary steps.

```bash
# initialize app
copilot app init npmrd-curator --domain liningtonlab.org
# initialize environment
# reuse VPC with Database instance already available
copilot env init --profile default -n test --import-vpc-id vpc-0530664f66042736c\
    --import-public-subnets subnet-0311041651e4d69e5,subnet-09d0b1ede80d70c58\
    --import-private-subnets subnet-0eb49e353d7d90c6d,subnet-09f584e905d571da5

# Need to add security group to DB access sg - do in console...

# Add the DB postgres URI to AWS secret manager
# follow the prompts and set the name=POSTGRES_URI
# and the value should look like postgresql://USERNAME:PASSWORD@URL:5432/npmrd_curator
copilot secret init

# Launch Backend
copilot init  -a npmrd-curator -n backend -d ./backend/Dockerfile -t "Load Balanced Web Service" --deploy

# Launch Frontend
copilot init  -a npmrd-curator -n frontend -d ./backend/Dockerfile -t "Load Balanced Web Service" --deploy
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
