DOCKER_COMPOSE_FILE=./docker-compose.yml
VOLUMES=./volumes

docker compose -f $DOCKER_COMPOSE_FILE down --volumes
find . -type d -name 'migrations' -exec rm -r {} +
find . -type f -name 'db.sqlite3' -exec rm {} +

sudo rm -rf $VOLUMES
make volumes
docker compose -f $DOCKER_COMPOSE_FILE up --build -d chat usermanagement db gateway

#psql -U ${DB_USER} -d ${DB_NAME}