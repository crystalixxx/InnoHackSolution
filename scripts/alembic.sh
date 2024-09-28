#!/bin/bash

# Exit in case of error
set -e

docker compose build

docker compose up -d
docker compose run --rm backend alembic revision --autogenerate
docker compose down