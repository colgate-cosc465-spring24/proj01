#/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: ./docker_exec.py COMMAND"
    exit 1
fi

COMMAND=$*

docker exec --tty ${USER}_proxy $COMMAND
