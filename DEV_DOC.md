# DEV_DOC — Inception

## Overview

This document describes how a developer can set up, build, run, and manage the Inception project.  
It focuses on the development environment, container management, and data persistence.

---

## Environment Setup

### Prerequisites

The following tools must be installed on the host system:

- Docker
- Docker Compose
- Make

You can verify installation with:
```bash
docker --version
docker compose version
make --version
```

## Configuration Files

The project configuration is based on the following files:

Dockerfile for each service (NGINX, WordPress, MariaDB)

docker-compose.yml to to manage containers

.env file to define environment variables


## Environment Variables and Secrets

Environment variables are defined in the .env file at the root of the project.

This file contains:

Database credentials

WordPress credentials

Domain configuration


## Building and Launching the Project
1 To build Docker images and start all services:

```bash
make build
```
2 To stop the services:

```bash
make down
```

3 clean the environment:
```bash
make clean
```

## Container and Volume Management

1 List Running Containers

```bash
make ps
```

2 Access a Container
```bash
docker exec -it <container_name> bash
```

## Data Storage and Persistence
1 Volumes are managed automatically by Docker and can be listed with:

```bash
docker volume ls
```