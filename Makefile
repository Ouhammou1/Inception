NAME = nginx-compose

DC = docker compose
FILE = srcs/docker-compose.yml

all: up

up:
	$(DC) -f $(FILE) up -d

down:
	$(DC) -f $(FILE) down

start:
	$(DC) -f $(FILE) start

stop:
	$(DC) -f $(FILE) stop

restart:
	$(DC) -f $(FILE) down
	$(DC) -f $(FILE) up -d

logs:
	$(DC) -f $(FILE) logs -f

ps:
	$(DC) -f $(FILE) ps

clean:
	$(DC) -f $(FILE) down -v

re: clean up

.PHONY: all up down start stop restart logs ps clean re
