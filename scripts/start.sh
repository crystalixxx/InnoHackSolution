#!/bin/bash

# Exit in case of error
set -e

docker compose build

# Build and run containers
docker compose up

# Hack to wait for postgres container to be up before running alembic migrations
sleep 5;

docker compose run --rm backend alembic upgrade head