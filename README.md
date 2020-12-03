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
