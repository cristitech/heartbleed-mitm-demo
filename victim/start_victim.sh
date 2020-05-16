#!/bin/bash
DID=$(sudo docker ps -a | grep "cristitech/victim" | cut -d " " -f 1 )
sudo docker exec -it $DID /bin/bash
