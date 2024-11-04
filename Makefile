# Makefile for Docker Compose commands

# Variables
DEEPEVAL := ${PWD}/.venv/bin/deepeval
DOCKER_COMPOSE ?= docker-compose  # Allows overriding the docker-compose executable
COMPOSE_FILE := docker-compose.yml

# Docker Compose commands
.PHONY: up down restart build logs log-chainlit ps stop start clean test clear-cache help

up:  ## Start services in detached mode
	@echo "Services are starting..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d

down:  ## Stop and remove containers
	@echo "Services are stopping..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down

restart:  ## Restart services
	@echo "Services have restarted..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up -d

build:  ## Build or rebuild services
	@echo "Services are being built..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build

logs:  ## Follow logs of running services
	@echo "Tailing logs..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

log-chainlit:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f chainlit

ps:  ## List containers
	@echo "Listing all services..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps -a

stop:  ## Stop services without removing containers
	@echo "Services are stopped..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop

start:  ## Start stopped services
	@echo "Services are started..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) start

clean:  ## Stop services and remove containers and volumes
	@echo "Services and volumes have been removed..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down --volumes

test:
	@echo "Running tests..."
	@$(DEEPEVAL) test run ./tests/

clear-cache:
	@echo "Clearing cache..."
	rm -rf volumes/chainlit/cache/*

help:  ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
