* This project has been created as part of the 42 curriculum by bouhammo

# inception 

## Description
**Inception** is a system administration project from the 42 curriculum focused on containerization using Docker.
It requires building  multiple services (NGINX, WordPress, MariaDB) from scratch using Dockerfiles and Docker Compose.
The goal is to understand Docker, networking, volumes, and service isolation in a real production-like setup


## Instructions
### Prerequisites

Make sure the following tools are installed on your system:

- Docker
- Docker Compose
- Make

You can verify the installation with:
```bash
docker --version
docker compose version
make --version

```

### Installation

1 . Clone the repository
```bash
git clone  https://github.com/Ouhammou1/Inception.git inception 
cd inception 
```

2 . Create the required environment variables file:

```bash
touch  .env
```

3 . Edit the .env file and add the following variables
```env
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_ROOT_PASSWORD=
MYSQL_HOST=

# WordPress variables
DOMAIN_NAME=
WP_ADMIN_USER=
WP_ADMIN_PASSWORD=
WP_ADMIN_EMAIL=

WP_USER=
WP_USER_EMAIL=
WP_USER_PASSWORD=

```


### Execution
1 To build and start all services:

```bash
make build
```
2 To stop the services:

```bash
make down
```

3 To completely clean the environment (containers, volumes, images):

```bash
make clean
```

### Verification 
1 Check running containers:

```bash
make ps
```

2  Open in browser :

```text
https://bouhammo.42.fr

```

### Troubleshooting

1 To inspect logs of a specific service:

```bash
make logs
```

2 To enter a running container:

```bash
docker exec -it <container_name> bash
```

3 This removes all unused Docker data.

```bash
docker system prune -a --volumes -f
```


## Resources

### Documentation & References

- Docker Documentation  
  https://docs.docker.com

- Docker Compose Documentation  
  https://docs.docker.com/compose

- NGINX Documentation  
  https://nginx.org/en/docs

- WordPress Documentation  
  https://wordpress.org/support/

- MariaDB Documentation  
  https://mariadb.com/kb/en/documentation/

- Inception Guide – 42 Project (Part I)  
  https://medium.com/@ssterdev/inception-guide-42-project-part-i-7e3af15eb671

- Inception Guide – 42 Project (Part II)  
  https://medium.com/@ssterdev/inception-42-project-part-ii-19a06962cf3b

- Grademe Inception Tutorial  
  https://tuto.grademe.fr/inception/

These resources were used to understand Docker fundamentals, container networking, volume management, service configuration, and the specific requirements of the 42 Inception project.

---

### Use of AI

AI tools (ChatGPT and Deepseek) were used during the development of this project for the following purposes:

- Understanding Docker and Docker Compose concepts  
- Clarifying system administration and networking principles
- Assisting with debugging configuration issues (Dockerfiles, NGINX, Docker Compose)  



## Project Description

### Use of Docker

Docker is used to run each service in its own container, allowing clear separation between components.  
This approach improves reliability, simplifies maintenance, and ensures consistent behavior across environments.  
Containers communicate through Docker’s internal networking system.

---

### Project Sources

- Dockerfiles for building custom images  
- `docker-compose.yml` for managing and launching services  
- Service configuration files and startup scripts  

---

### Design Decisions

Each service is isolated in a separate container to avoid dependency conflicts.  
A dedicated Docker network is used to allow controlled communication between services.  
Docker volumes are used to store persistent data and prevent data loss when containers are restarted.

---

## Technical Comparisons

### Virtual Machines vs Docker

Virtual Machines include a full operating system, making them heavier and slower to start.  
Docker containers share the host system kernel, making them lighter, faster, and more efficient for this project.

---

### Secrets vs Environment Variables

Environment variables provide an easy way to configure services but offer limited security.  
Secrets provide better protection for sensitive data by keeping it separate from the application configuration.

---

### Docker Network vs Host Network

Docker networks isolate container communication and reduce security risks.  
Host networking removes this isolation and directly exposes services to the host system.

---

### Docker Volumes vs Bind Mounts

Docker volumes are managed by Docker and are well suited for persistent container data.  
Bind mounts link directly to host files, which is useful for development but less safe in production environments.
