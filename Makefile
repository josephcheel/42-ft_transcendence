COMPOSE = docker compose

DOCKER_COMPOSE_FILE = ./docker-compose.yml
include .env
VOLUMES = ${VOLUMES_FOLDER} ${CERTS_FOLDER} ${ESDATA_FOLDER} ${KIBANA_FOLDER} ${LOGSTASH_FOLDER} ${POSTGREE_FOLDER} ${PROMETHEUS_FOLDER} ${GRAFANA_FOLDER}
LOG_FILES =  $(addprefix ${LOGSTASH_FOLDER}, ${GATEWAY_LOG} ${USER_LOG} ${CHAT_LOG} ${GAMESTATS_LOG} ${TWOFACTOR_LOG})

# Define targets
all: build 

build: 	| volumes
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build

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

rebuild:
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --volumes
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build -d



volumes: 
	@echo Creating Volumes DIR
	@mkdir -p $(VOLUMES)
	@touch $(LOG_FILES)

clean: stop
	
fclean: clean
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --rmi all --volumes

	@docker system prune -af 
	@sudo rm -rf $(VOLUMES)

re: fclean all




.PHONY: all build up down restart logs clean re fclean volumes



