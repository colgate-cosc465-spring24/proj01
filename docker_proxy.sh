#/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./docker_proxy.py PROXY_PORT"
    exit 1
fi

PROXY_PORT=$1

docker image remove "${USER}_proxy"
docker build --rm --tag="${USER}_proxy" .
docker run --tty --interactive --rm --publish=$PROXY_PORT:$PROXY_PORT --name=${USER}_proxy ${USER}_proxy python ./proxy.py -p $PROXY_PORT
