# npmrd_curator

Backend + Frontend for NP-MRD curator applet.

## DB

This app runs on a small database. You will need to modify the `api` service in `docker-compose.yml`
to either point to a file based sqlite database (persisted through a shared file mount in docker),
or configure the `POSTGRES_URI` environment variable (REMOVE this variable if you are not using an
external database or the app will fail to launch due to a psql connection error).

The app (via SQLAlchemy) should automatically handle setting up the necessary tables. It will not however
create a postgres database for you (it must be able to connect).

## Getting Data

There is a script located at `./backend/get_npmrd_curator_data.py`. You will need to be connected to the AWS VPC through
our VPN solution to interact with the npmrd_curator database server. The script will automatically retrieve all previously unhandled
data, write them to `./submissions/npmrd_curator_SESSIONID.json` file and ask you if you'd like to mark these new entries as handled. 
A `handled` entry, should be sent to the NP-MRD database **ASAP** or be tracking in some other meaning full name.

### Copilot Deployment

AWS Copilot has been used to deploy this stack into an existing VPC so that we can connect to a central RDS instance.

Make sure to initialize backend before frontend or DNS rules will cause an issue...
    
* Matt's Note: This extends to redeployment as well. Whenever the backend is redeployed ensure that you redeploy the frontend AFTER the backend is fully redeployed (even if you've made no changes to the frontend). Otherwise they will not be able talk to one another

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
copilot secret init --name POSTGRES_URI

# Make sure to initialize backend before frontend or DNS rules will cause an issue...
# Launch Backend
copilot init  -a npmrd-curator -n backend -d ./backend/Dockerfile -t "Load Balanced Web Service" --deploy

# Launch Frontend
copilot init  -a npmrd-curator -n frontend -d ./frontend/Dockerfile -t "Load Balanced Web Service" --deploy
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

### Running both locally
When you want to test the frontend and backend such that they can talk to each other go to the base directory of the project (where `docker-compose.yml` is located) first go into the frontend's `nuxt.conifg.js` and unmute this line. NOTE: Always make sure you re-mute this before deploying.

```
  proxy: {
    // '/api/': 'http://localhost:80/',
  },
```

Now, run...

```
docker compose up
```

After you've done that you should see status reports for the frontend and backend launching correctly. Now you can go to the frontend via `localhost:80` and test away!

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

pipenv can be activated locally by running...
```
pipenv shell
```

## Testing

Python tests can be run using the `pytest` framework.


## Pushing Data To NP Deposition

Scripts have been bolted on top of existing functionality to simply make this system push data to the NP Deposition platform.

First, entries have received a `handled` bool value which indicates whether they have been pushed to NP deposition or not. This defaults to false.

First, the `add_mol_block.py` script runs to record some key information, namely the addition of "canonicalized_mol_block" and surrounding information.

Then `push_submission_to_npmrd.py` runs to directly push jsons representing curations to an api endpoint in the npdeposition platform as well as to push archival copies to and s3 bucket. Within this file is a setting you can configure called "MAX_ENTRIES_TO_PUSH" which will set a ceiling on the number of curation jsons that are pushed whenever this script is run.

To run these manually connect to the container using...

```
copilot svc exec
```

Then within the container

```
. /app/env.sh
export PYTHONPATH=/app

python json_extraction_scripts/add_mol_block.py
# OR
python json_extraction_scripts/push_submissions_to_npmrd.py
```

These are also setup to run with crontab jobs every hour so that any new curations will be automatically pushed to npdeposition.

