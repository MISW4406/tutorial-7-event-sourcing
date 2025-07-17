#!/bin/bash
set -e

# Create required directories and set permissions
mkdir -p data/bookkeeper
mkdir -p data/zookeeper
mkdir -p data/mysql
sudo chmod -R 777 ./data
sudo chmod -R 777 ./connectors

# Build docker images for local development
if command -v docker >/dev/null 2>&1; then
  docker build . -f aeroalpes.Dockerfile -t aeroalpes/flask
  docker build . -f adaptador.Dockerfile -t aeroalpes/adaptador
  docker build . -f notificacion.Dockerfile -t aeroalpes/notificacion
  docker build . -f ui.Dockerfile -t aeroalpes/ui
  docker-compose pull || true
fi
