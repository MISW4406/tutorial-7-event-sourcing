#!/bin/bash
set -e

# Create required directories and set permissions
mkdir -p data/bookkeeper
mkdir -p data/zookeeper
mkdir -p data/mysql
sudo chmod -R 777 ./data
sudo chmod -R 777 ./connectors
