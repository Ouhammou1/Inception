# USER_DOC — Inception

## Overview

This document explains how to use and manage the **Inception** project as an end user or administrator.  
The project provides a containerized web stack using Docker.

---

## Provided Services

The stack includes the following services:

- **NGINX**  
  Acts as a web server and reverse proxy, handling HTTPS connections.

- **WordPress**  
  A content management system (CMS) used to manage and display the website.

- **MariaDB**  
  A relational database used to store WordPress data.

All services run in separate Docker containers and communicate through a private Docker network.

---

## Starting the Project

To start the project, make sure you are in the root directory of the repository.

1 Build and launch all services:

```bash
make build
```
## Stopping the Project
1 To stop the services:

```bash
make down
```

2 To completely clean the environment (containers, volumes, images):

```bash
make clean
```

## Accessing the Website

1 Add the domain to your host file:

```bash
127.0.0.1   bouhammo.42.fr
```

2 Open the website in your browser:

```text
https://bouhammo.42.fr

```
## Accessing the Administration Panel
```bash
https://bouhammo.42.fr/wp-admin
```

## Managing Credentials

All credentials are stored in the .env file located at the root of the project.

This file contains:

Database credentials

WordPress administrator credentials

WordPress user credentials


## Checking Service Status

1 To check if the services are running correctly:
```bash
make ps
```

2 To enter a running container:

```bash
docker exec -it <container_name> bash
```