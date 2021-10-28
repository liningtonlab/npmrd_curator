#! /bin/bash
docker-compose build
docker push ghcr.io/liningtonlab/npmrd_curator_app:latest
docker push ghcr.io/liningtonlab/npmrd_curator_api:latest