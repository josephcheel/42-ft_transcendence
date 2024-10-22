ifeq ($(MAKECMDGOALS), debug)
  DEBUG := True
else
  DEBUG := False
endif

export DEBUG
include .env

COMPOSE = docker compose
LIST_CURRENT_VOLUMES=$(shell docker volume ls -q)

DOCKER_COMPOSE_FILE = ./docker-compose.yml
VOLUMES = ${VOLUMES_FOLDER} ${CERTS_FOLDER} ${ESDATA_FOLDER} ${KIBANA_FOLDER} ${LOGSTASH_FOLDER} ${POSTGREE_FOLDER} ${PROMETHEUS_FOLDER} ${GRAFANA_FOLDER} ${BLOCKCHAIN_FOLDER} ${TOURNAMENTS_FOLDER}
LOG_FILES =  $(addprefix ${LOGSTASH_FOLDER}, ${GATEWAY_LOG} ${USER_LOG} ${CHAT_LOG} ${MATCHES_LOG} ${TOURNAMENT_LOG})

# Define targets
all: build 

build: 	| volumes
	cp .env ./frontend/.env
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build -d

down:
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

restart:
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) restart

logs:
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f

stop : 
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop

start : 
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) start

rebuild: rm_files

	@mkdir -p $(VOLUMES)
	@touch $(LOG_FILES)
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build -d

rm_files:
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --volumes
	@sudo find . -type d -name 'migrations' -exec rm -r {} +
	@sudo find . -type d -name '__pycache__' -exec rm -r {} +
	@sudo find . -type f -name 'db.sqlite3' -exec rm {} +
	@sudo rm -rf $(VOLUMES)

migrat:
	docker exec -it migrations /bin/bash

tour:
	docker exec -it tournaments /bin/bash

user:
	docker exec -it usermanagement /bin/bash

bch:
	docker exec -it blockchain /bin/bash

gate:
	docker exec -it gateway /bin/bash

work:
	docker exec -it celery_worker /bin/bash

volumes: 
	@echo Creating Volumes DIR
	@mkdir -p $(VOLUMES)
	@touch $(LOG_FILES)

del_vol:rm_vol
	@echo Deleting Volumes DIR
	@suifeq ($(MAKECMDGOALS), debug)

rm_vol:
	@if [ -n "$(LIST_CURRENT_VOLUMES)" ]; then \
        echo "Removing Docker volumes: $(LIST_CURRENT_VOLUMES)"; \
        docker volume rm $(LIST_CURRENT_VOLUMES); \
    else \
        echo "No Docker volumes to remove"; \
    fi
	sudo find . -type d -name 'migrations' -exec find {} -type f -delete \;
	sudo find . -type d -name '_pycache_' -exec rm -r {} +
	sudo find . -type f -name 'db.sqlite3' -exec rm {} +

clean: stop
	
fclean: clean rm_files
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --rmi all --volumes
	@docker system prune -af 
	@sudo rm -rf $(VOLUMES)

re: fclean all




.PHONY: all build up down restart logs clean re fclean volumes