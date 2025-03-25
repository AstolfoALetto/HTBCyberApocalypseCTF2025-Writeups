#!/bin/bash
docker build -t lyras_tavern .
docker run  --name=lyras_tavern --rm -p 80:3000 -p 445:445 -it lyras_tavern