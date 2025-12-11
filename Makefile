NAME = inception

DC = docker compose
FILE = srcs/docker-compose.yml

DATA_DIR = /home/bouhammo/data

WP_DIR = $(DATA_DIR)/wp
DB_DIR = $(DATA_DIR)/maria

all: prepare up

prepare:
	@mkdir -p $(WP_DIR)
	@mkdir -p $(DB_DIR)

up:
	$(DC) -f $(FILE) up #-d

build:
	$(DC) -f $(FILE) up --build -d

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

re: clean build
