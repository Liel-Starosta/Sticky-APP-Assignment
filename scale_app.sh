#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_replicas>"
    exit 1
fi

REPLICAS=$1

docker-compose up -d --scale app=$REPLICAS

