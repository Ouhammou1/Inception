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
1 Explained in Building and Launching the Project:

```bash
make
```
This command:

- Builds Docker images

- Creates networks and volumes

- Launches all services using Docker Compose


2 Stopping and cleaning:
```bash
make down
make clean
```

## Use relevant commands to manage containers and volumes

### Container Management

1 Explained in Container Management:
- List containers:
```bash
make ps
```

- Access a Container
```bash
docker exec -it <container_name> bash
```

### Volume Management
1 Explained in Volume Management:
- List volumes:
```bash
docker volume ls
```

- Inspect volume:
```bash
docker volume inspect <volume_name>
```
- Remove volumes:
```bash
docker volume prune
```


## Identify where project data is stored and how it persists
Explained in Volume Management
- MariaDB data:
```bash
/var/lib/mysql
```
- WordPress data:

```bash
/var/www/html
```
