#!/bin/bash
# (c) 2020 Cristian Negru

# CAUTION: Removes all docker containers & docker images
for id in `sudo docker ps -a | tail -n+2 | awk '{print $1}'`; do docker stop $id; docker rm $id;  done
for id in `sudo docker images | tail -n+2 | awk '{print $3}'`; do docker image rm $id; done
