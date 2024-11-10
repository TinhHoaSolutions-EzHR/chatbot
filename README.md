# EzHr-Chatbot LLM-based Assistant

This is the LLM-based assistant for the EzHr-Chatbot project. It makes use of RAG and LlamaIndex to provide a conversational interface for the users.

## Authors

- Meow

## Components

### API Server

This is the API server for the EzHr-Chatbot LLM-based assistant. It is built using FastAPI and LlamaIndex for LLM framework coding.

For developing and testing purposes, we can use the Docker compose to run the API server.

```bash
# Move to the docker_compose directory
cd deployment/docker_compose

# Create the environment file
cp .env.example .env

# Build the docker image
docker-compose build

# Run the docker container
docker-compose up -d
```

Nhan beo

