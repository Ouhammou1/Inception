NAME = inception

DC = docker compose
FILE = srcs/docker-compose.yml

DATA_DIR = /home/bouhammo/data

HOSTNAME = bouhammo.42.fr
HOSTS_LINE = 127.0.0.1   $(HOSTNAME)


all: create_volumes add_host  up 

add_host:
	@if grep -q "$(HOSTNAME)" /etc/hosts; then \
		echo "$(HOSTNAME) already exists in /etc/hosts"; \
	else \
		echo "$(HOSTS_LINE)" | sudo tee -a /etc/hosts > /dev/null; \
		echo "$(HOSTNAME) added to /etc/hosts"; \
	fi


create_volumes:
	@sudo mkdir -p $(DATA_DIR)/wp
	@sudo mkdir -p $(DATA_DIR)/maria
	@sudo chown -R 999:999 $(DATA_DIR)/maria
	@sudo chown -R 1000:1000 $(DATA_DIR)/wp




up:
	$(DC) -f $(FILE) up  --build -d


down:
	$(DC) -f $(FILE) down 

start:
	$(DC) -f $(FILE) start

stop:
	$(DC) -f $(FILE) stop

restart:
	$(DC) -f $(FILE) down -v 
	$(DC) -f $(FILE) up  --build -d

logs:
	$(DC) -f $(FILE) logs -f

ps:
	$(DC) -f $(FILE) ps -a

clean:
	$(DC) -f $(FILE) down -v
	@sudo rm -rf $(DATA_DIR)/*



re: clean up