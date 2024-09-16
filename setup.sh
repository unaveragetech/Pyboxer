#!/bin/bash

# Update package manager
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Verify Docker is installed
docker --version

# Set environment variables for Docker in .env file for Replit
DOCKER_HOST="tcp://localhost:2376"
DOCKER_CERT_PATH="/etc/docker/certs"
DOCKER_TLS_VERIFY="1"

# Writing to environment file
echo "DOCKER_HOST=$DOCKER_HOST" >> .env
echo "DOCKER_CERT_PATH=$DOCKER_CERT_PATH" >> .env
echo "DOCKER_TLS_VERIFY=$DOCKER_TLS_VERIFY" >> .env

# Add Docker group to user
sudo usermod -aG docker $USER

# Print success message
echo "Docker installation complete. Make sure to restart the terminal for changes to take effect."
