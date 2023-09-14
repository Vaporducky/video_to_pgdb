#!/bin/bash
# Export .env file
eval $(egrep "^[^#;]" .env | xargs -d'\n' -n1 | sed 's/^/export /')
PG_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DOCKER_PORT}/${POSTGRES_DB}"
export PG_URI
# Set up Postgres container

# Build image if not built
if [ "$(docker images --format "{{.Repository}}" ${DOCKER_IMAGE})" != "${DOCKER_IMAGE}" ]; then
  docker build -t ${DOCKER_IMAGE} "${METADATA_PATH}/database" && echo -e "Docker image sucessfully built.\n\n" && docker images ${DOCKER_IMAGE} && echo -e "\n"
fi

# Start container
docker run --rm -d --env-file=.env_db -p $HOST_PORT:$DOCKER_PORT --name=$CONTAINER_NAME ${DOCKER_IMAGE}

# Wait until container is ready
while [ "$(docker inspect -f {{.State.Running}} ${CONTAINER_NAME})" != "true" ]; do
  sleep 2;
done

echo "======================================================================================"
echo "Container ready: $(docker inspect -f {{.State.Running}} ${CONTAINER_NAME})"
echo "Connect to the database using the following command:"
echo "docker exec -it pg_container psql ${PG_URI}"
echo "======================================================================================"

sleep 10

# Create database table
"${PYENV_ROOT}/versions/${PYENV_NAME}/bin/python" ./src/dependencies/metadata_schema.py

