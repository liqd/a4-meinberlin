# Docker Setup for mein.berlin

This document provides instructions for setting up the mein.berlin project using Docker, which provides a consistent development environment across all operating systems.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository
`git clone git@github.com:liqd/a4-meinberlin.git`
2. Navigate to the project directory
`cd a4-meinberlin`
3. Make the Docker script executable:
`chmod +x docker-make.sh`

4. Build and start the containers:
`./docker-make.sh install`
`./docker-make.sh up`

5. The application will be available at http://localhost:8003

## Common Commands

Use the `docker-make.sh` script to run common tasks:

```bash
# Start all containers
./docker-make.sh up

# Stop all containers
./docker-make.sh down

# Load fixtures
./docker-make.sh fixtures

# Run tests
./docker-make.sh test

# Run Python tests only
./docker-make.sh pytest

# Run JS tests only
./docker-make.sh jstest

# Run linters
./docker-make.sh lint

# Open a shell in the web container
./docker-make.sh shell

# Run Django manage.py commands
./docker-make.sh manage [command]
# Example: ./docker-make.sh manage createsuperuser

# Run npm commands
./docker-make.sh npm [command]
# Example: ./docker-make.sh npm run build

# Clean up everything (including volumes)
./docker-make.sh clean