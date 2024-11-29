# EzHr-Chatbot LLM-based Assistant

This is the LLM-based assistant for the EzHr-Chatbot project. It makes use of RAG and LlamaIndex to provide a conversational interface for the users.

## Components

### API Server

This is the API server for the EzHr-Chatbot LLM-based assistant. It is built using FastAPI and LlamaIndex for LLM framework coding.

For developing and testing purposes, we can use the Docker compose to run the API server.

Go to the chatbot-core directory

```bash
cd chatbot-core
```

Create the environment file from example

```
cp .env.example .env
```

Build the docker image

```
make build
# Or
docker compose -f ../deployment/docker_compose/docker-compose.dev.yaml -p chatbot-core build
```

Run the docker container

```
make up
```

Ping the API Server

```
curl http://localhost:5000/ping | jq
```

Every necessary commands are in the Makefile. You can use `make help` to see all available commands.
