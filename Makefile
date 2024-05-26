.EXPORT_ALL_VARIABLES:
COMPOSE_FILE ?= ./build/docker-compose/docker-compose.yml
BOT_SERVICE ?= bot

DOTENV_BASE_FILE ?= .env
-include $(DOTENV_BASE_FILE)

.PHONY: start-bot
start-bot: build-bot up

.PHONY: up
up:
	docker compose -f $(COMPOSE_FILE) up -d
	docker compose ps

.PHONY: restart
restart: down up logs

.PHONY: down
down:
	docker compose down

.PHONY: logs
logs:
	docker compose logs --follow

.PHONY: connect
connect:
	docker compose exec -it $(BOT_SERVICE) /bin/bash

.PHONY: run-lints
run-lints: lint-black lint-flake

.PHONY: lint-black
lint-black:
	docker compose -f $(COMPOSE_FILE) run --rm $(BOT_SERVICE) black .

.PHONY: lint-flake
lint-flake:
	docker compose -f $(COMPOSE_FILE) run --rm $(BOT_SERVICE) flake8 .

.PHONY: build-bot
build-bot:
	docker build \
		--tag=tasks_bot \
		--file=build/docker/Dockerfile \
		.
