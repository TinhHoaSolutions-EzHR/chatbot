# EzHr-Chatbot LLM-based Assistant

This is the LLM-based assistant for the EzHr-Chatbot project. It makes use of RAG and LlamaIndex to provide a conversational interface for the users.

## Installation

### Prerequisites

- Python >= 3.11.10 (specified at `.tool-versions` and `pyproject.toml`)
- uv >= 0.5.26. [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- Docker and Docker Compose. [Installation guide](https://docs.docker.com/get-docker/)
- NodeJS >= 16.13.0 (specified at `.tool-versions`) and yarn (optional)

### Setup installation

For developing and testing purposes, we can use the Docker compose to run the API server.

1. Go to the root directory

2. Create the environment file from example

```bash
cp .env.example .env
```

(Optional) If you want to use [direnv](https://direnv.net/), you can use the .envrc file

```bash
direnv allow
```

Then the environment variables from `.env` will be loaded and unloaded when you enter and exit the directory.

If you don't want to use direnv, you can go ahead with the `.env` file.

3. Build the docker image:

```bash
make build
# Or this command
docker compose -f ../deployment/docker_compose/docker-compose.dev.yaml -p chatbot build
```

4. Run the docker container

```bash
make up
```

5. Ping the API Server

```bash
curl http://localhost:5000/health | jq
```

6. For more commands, you can use the [Makefile](./Makefile)

```bash
make help
```

7. To stop the container

```bash
make down
```

8. To remove the container

```bash
make clean
```

Every necessary commands are in the Makefile. You can use `make help` to see all available commands.

## Components

### API Server

This is the backend API server for the EzHr-Chatbot LLM-based assistant. It is built using FastAPI and LlamaIndex for LLM framework coding.
