DOCKER_COMPOSE_FILE=./docker-compose.yml
VOLUMES=./volumes

docker compose -f $DOCKER_COMPOSE_FILE down --volumes
sudo rm -rf $VOLUMES
make volumes
docker compose -f $DOCKER_COMPOSE_FILE up --build -d gateway usermanagement db

#psql -U ${DB_USER} -d ${DB_NAME}