#!/bin/bash
apt install docker-io -y
apt install docker-compose -y
export BACKEND_IMAGE_NAME="backend:latest"
export FRONTEND_IMAGE_NAME="frontend:latest"
#docker-compose build
docker-compose up

