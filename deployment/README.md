# Deploying EzHR

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Deployment

1. Navigate to the `deployment\docker_compose` directory.
2. Run the following command to start the services:

```bash
docker compose -f docker-compose.dev.yaml -p ezhr up --build --force-recreate -d
```

3. Access the application at [http://localhost:3000](http://localhost:3000) or [http://localhost:8000/](http://localhost:8000/).

## Stopping the Services

To stop the services, run the following command:

```bash
docker compose -f docker-compose.dev.yaml -p ezhr stop
```

## Removing the Services

To remove the containers, run the following command:

```bash
docker compose -f docker-compose.dev.yaml -p ezhr down
```

This will remove the containers and the volumes associated with the services.

```basg
docker compose -f docker-compose.dev.yaml -p ezhr down -v
```

