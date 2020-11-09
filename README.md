# npmrd_curator

Backend + Frontend for NP-MRD curator applet.

## Running

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

```bash
conda env create -f environment.yml
```

```bash
cd npmrd_curator_app
yarn
```
