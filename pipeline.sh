#!/bin/bash

URL_FILE="$1"
echo $URL
eval $(egrep "^[^#;]" .env | xargs -d'\n' -n1 | sed 's/^/export /')
PG_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DOCKER_PORT}/${POSTGRES_DB}"
export PG_URI

# Use virtual environment to execute Python code
"${PYENV_ROOT}/versions/${PYENV_NAME}/bin/python" ./src/main.py --url-file ${URL_FILE}

