# build and run docker containers via docker compose, using the settings in both the base docker-compose file and docker-compose.dev to use automatic sync features
dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --watch

# run dockerization in a prod environment, disabling watch and sync features and binding host 443 to the nginx container
prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# create a self signed cert for https
dev-cert:
	#!/usr/bin/env sh
	mkdir -p ./certs
	openssl req -x509 -nodes -days 365 \
	-newkey rsa:2048 \
	-keyout ./certs/privkey.pem \
	-out ./certs/fullchain.pem \
	-subj "/CN=localhost"

