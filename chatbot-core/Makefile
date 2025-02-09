# Makefile for Docker Compose commands

# Variables
DEEPEVAL := ${PWD}/backend/.venv/bin/deepeval
DOCKER_COMPOSE ?= $(shell command -v docker-compose 2>/dev/null || echo docker compose)  # Allows overriding the docker-compose executable
COMPOSE_FILE := ../deployment/docker_compose/docker-compose.dev.yaml
YARN ?= yarn
UV ?= uv
SERVICES ?=  # List of services to start, default is empty (all services)
COMMAND ?= sh  # Command to run in the container, default is sh

# Docker Compose commands
.PHONY: up down pause unpause exec restart build logs ps stop start clean alembic-revision alembic-upgrade-head test shell help

up:  ## Start services in detached mode
	@echo "Services are starting..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core up -d; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core up -d $(SERVICES); \
	fi

down:  ## Stop and remove containers
	@echo "Services are stopping..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core down

pause:  ## Pause services
	@echo "Services are paused..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core pause

unpause:  ## Unpause services
	@echo "Services are unpaused..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core unpause

exec:  ## Run a command in a running container
	@echo "Running command in container..."
	@if [ -z "$(SERVICES)" ]; then \
		echo "Error: SERVICES is not set. Provide it using make exec SERVICES=<one service> [COMMAND=<command>]"; \
		exit 1; \
	else \
		echo "Executing command '$(COMMAND)' in service '$(SERVICES)'..."; \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core exec $(SERVICES) $(COMMAND); \
	fi

restart:  ## Restart all services
	@echo "Services have restarted..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core down
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core up -d

build:  ## Build or rebuild services
	@echo "Services are being built..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core build; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core build $(SERVICES); \
	fi

logs:  ## Follow logs of running services
	@echo "Tailing logs..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core logs -f; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core logs -f $(SERVICES); \
	fi

ps:  ## List containers
	@echo "Listing all services..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core ps -a

status:  ## Show status of services
	@echo "Showing status of services..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core ps; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core ps $(SERVICES); \
	fi

stop:  ## Stop services without removing containers
	@echo "Services are stopped..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core stop; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core stop $(SERVICES); \
	fi

start:  ## Start stopped services
	@echo "Services are started..."
	@if [ -z "$(SERVICES)" ]; then \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core start; \
	else \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core start $(SERVICES); \
	fi

clean:  ## Stop services and remove containers and volumes
	@echo "Services and volumes have been removed..."
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core down -v

alembic-revision:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core exec api-server uv run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

alembic-upgrade-head:
	@$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core exec api-server uv run alembic upgrade head

test:  ## TODO: Run tests
	@echo "Running tests..."

shell:  ## Open a shell in a specified service
	@if [ -z "$(SERVICES)" ]; then \
		echo "Error: SERVICES is not set. Provide it using make shell SERVICES=<service>"; \
		exit 1; \
	else \
		echo "Opening a shell in service '$(SERVICES)'..."; \
		$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) -p chatbot-core exec $(SERVICES) sh; \
	fi

help:  ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo
	@echo "Environment variables:"
	@echo "  SERVICES     List of services to start (default: all)"
	@echo "  COMMAND      Command to execute within a service (default: sh)"

%: ## Prevents make from throwing an error when a target is not found
	@:
