#!/bin/bash

# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Remove all networks
docker network rm $(docker network ls -q)

# Remove all build cache
docker builder prune -a -f

# Remove all unused data
docker system prune -a -f

# Rebuild and start Docker containers
docker compose up --build
