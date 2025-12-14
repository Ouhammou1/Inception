NAME = inception

DC = docker compose
FILE = srcs/docker-compose.yml

DATA_DIR = /home/bouhammo/data

create_volumes:
	sudo mkdir -p $(DATA_DIR)/wp
	sudo mkdir -p $(DATA_DIR)/maria
	sudo chown -R 1000:1000 $(DATA_DIR)/wp
	sudo chown -R 999:999 $(DATA_DIR)/maria
# sudo chmod -R 770 $(DATA_DIR)/maria

all: create_volumes up


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
	@sudo rm -rf $(DATA_DIR)/maria
	@sudo rm -rf $(DATA_DIR)/wp


re: clean build
