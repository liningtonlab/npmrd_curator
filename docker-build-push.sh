#! /bin/bash
docker-compose build
docker push registry.jvansan.duckdns.org/npmrd_curator_app:latest
docker push registry.jvansan.duckdns.org/npmrd_curator_api:latest