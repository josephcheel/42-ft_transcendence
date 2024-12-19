# COLORS 
RESET_COLOR=\033[0m
GREEN_COLOR=\033[32m
YELLOW_COLOR=\033[33m
RED_COLOR=\033[31m
BLUE_COLOR=\033[34m

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
VOLUMES = ${VOLUMES_FOLDER} ${LOGSTASH_FOLDER}
LOG_FILES =  $(addprefix ${LOGSTASH_FOLDER}, ${GATEWAY_LOG} ${USER_LOG} ${CHAT_LOG} ${MATCHES_LOG} ${TOURNAMENT_LOG})
CERTS=selfsigned.crt selfsigned.key

# Define targets
all: build 

build: 	| volumes build_certs copy_env #compile copy_env 
	$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --build -d

build_certs: $(CERTS)

$(CERTS):
	./cert.sh

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

rebuild: stop rm_files volumes build_certs copy_env build
	@echo "$(GREEN_COLOR)Rebuilding containers...$(RESET_COLOR)"

rm_files:
	@rm -rfd usermanagement/.migration_done
	@rm -rfd frontend/dist/
	@rm -rfd frontend/node_modules/
	@rm -f .exec_run_npm
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --volumes
	@find . -type d -name 'migrations' -exec rm -r {} +
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type f -name 'db.sqlite3' -exec rm {} +
	@rm -rf $(VOLUMES)


# Use 'make debug' to 'docker exec' a container 
debug:
	@if [ -z "$(container_name)" ]; then \
		echo "$(YELLOW_COLOR)Usage: make debug container_name=<container_name>$(RESET_COLOR)"; \
		exit 1; \
	fi
	@if ! docker ps -q -f name=$(container_name) > /dev/null; then \
		echo "$(RED_COLOR)Error: Container $(container_name) does not exist or is not running.$(RESET_COLOR)"; \
		exit 1; \
	fi
	@echo "$(BLUE_COLOR)Attempting to start bash in container $(container_name)...$(RESET_COLOR)"; \
	if ! docker exec -it $(container_name) /bin/bash; then \
		echo "$(YELLOW_COLOR)bash not found. Trying with sh...$(RESET_COLOR)"; \
		docker exec -it $(container_name) /bin/sh; \
	fi
	@echo "$(GREEN_COLOR)Debug session ended.$(RESET_COLOR)"

# Help target
help:
	@echo "$(BLUE_COLOR)Available Makefile targets:$(RESET_COLOR)"
	@echo "$(GREEN_COLOR)  all$(RESET_COLOR)           - Default target, builds the project."
	@echo "$(GREEN_COLOR)  build$(RESET_COLOR)         - Creates volumes, compiles code, and starts services with Docker Compose."
	@echo "$(GREEN_COLOR)  down$(RESET_COLOR)          - Stops and removes all containers managed by Docker Compose."
	@echo "$(GREEN_COLOR)  restart$(RESET_COLOR)       - Restarts all running containers."
	@echo "$(GREEN_COLOR)  logs$(RESET_COLOR)          - Streams logs from all containers."
	@echo "$(GREEN_COLOR)  stop$(RESET_COLOR)          - Stops running containers."
	@echo "$(GREEN_COLOR)  start$(RESET_COLOR)         - Starts stopped containers."
	@echo "$(GREEN_COLOR)  rebuild$(RESET_COLOR)       - Removes files, creates volumes, compiles code, and rebuilds containers."
	@echo "$(GREEN_COLOR)  rm_files$(RESET_COLOR)      - Removes temporary and generated files."
	@echo "$(GREEN_COLOR)  debug$(RESET_COLOR)         - Starts a bash shell (or sh as fallback) in a specified container."
	@echo "$(GREEN_COLOR)  volumes$(RESET_COLOR)       - Creates necessary volume directories and log files."
	@echo "$(GREEN_COLOR)  compile$(RESET_COLOR)       - Installs frontend dependencies using npm."
	@echo "$(GREEN_COLOR)  copy_env$(RESET_COLOR)       - Builds the frontend project using npm."
	@echo "$(GREEN_COLOR)  del_vol$(RESET_COLOR)       - Deletes Docker volumes and certain temporary files."
	@echo "$(GREEN_COLOR)  rm_vol$(RESET_COLOR)        - Removes Docker volumes and cleans up migrations and caches."
	@echo "$(GREEN_COLOR)  clean$(RESET_COLOR)         - Stops running containers."
	@echo "$(GREEN_COLOR)  fclean$(RESET_COLOR)        - Cleans and removes all data, images, and volumes."
	@echo "$(GREEN_COLOR)  re$(RESET_COLOR)            - Fully cleans and rebuilds the project from scratch."
	@echo "$(YELLOW_COLOR)Usage examples:$(RESET_COLOR)"
	@echo "  make build"
	@echo "  make debug container_name=<container_name>"
	@echo "  make clean"

# Other Makefile targets go here...

volumes: 
	@echo Creating Volumes DIR
	@mkdir -p $(VOLUMES)
	@touch $(LOG_FILES)

compile: ./frontend/package-lock.json 
	@npm --prefix ./frontend install
	@touch .exec_run_npm

copy_env:
	@cp .env ./frontend/.env
	@echo modifying .env ${IP_ADDR}
	@sed -i "s/^INT_IP_ADDR=changeme/IP_ADDR=${IP_ADDR}/" ./frontend/.env
	
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
	find . -type d -name 'migrations' -exec find {} -type f -delete \;
	find . -type d -name '_pycache_' -exec rm -r {} +
	find . -type f -name 'db.sqlite3' -exec rm {} +

clean: stop
	
fclean: clean rm_files
	@$(COMPOSE) -f $(DOCKER_COMPOSE_FILE) down --rmi all --volumes
	@docker system prune -af 
	@rm -rf $(VOLUMES)

re: fclean all


.PHONY: all build up down restart logs clean re fclean volumes compile run_pm del_vol rm_vol debug build_certs rebuild

