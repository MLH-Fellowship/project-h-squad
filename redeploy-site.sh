#!/bin/bash

cd project-h-squad-AnthonyH
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build