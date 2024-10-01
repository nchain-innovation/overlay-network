#!/bin/bash

DATA_DIR=$(realpath ../data)
SRC_DIR=$(realpath ./src)

# Start container
docker run -it \
    -p 3050:3050 \
    --mount type=bind,source=$SRC_DIR,target=/app/python \
    --mount type=bind,source=$DATA_DIR,target=/app/data \
    --rm example-app \
    $1 $2
