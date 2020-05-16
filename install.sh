#!/bin/bash

# Server (Vulnerable to heartbleed OpenSSL Library)
docker pull cristitech/docker-heartbleed

# Attacker
docker build -t cristitech/attacker ./attacker/

# Victim
docker build -t cristitech/victim ./victim/
