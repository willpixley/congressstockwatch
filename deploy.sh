#!/bin/bash
set -e

APP_DIR=/var/www/stocktracker
COMPOSE_FILE=docker-compose.yml  # production compose file

cd $APP_DIR

echo "Pulling latest code..."
git pull origin main

echo "Building containers..."
docker compose -f $COMPOSE_FILE build --pull

echo "Starting services..."
docker compose -f $COMPOSE_FILE up -d

echo "Pruning old images..."
docker image prune -f

echo "Deploy complete!"
