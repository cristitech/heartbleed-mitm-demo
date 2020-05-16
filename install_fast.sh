#!/bin/bash

# Server (Vulnerable to heartbleed OpenSSL Library)
docker pull cristitech/docker-heartbleed

# Attacker
docker pull cristitech/attacker

# Victim
docker pull cristitech/victim
