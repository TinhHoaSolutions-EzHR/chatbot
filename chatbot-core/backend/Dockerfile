# Use the official Python base image
FROM python:3.11.10-alpine

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container, including uv.lock
COPY . /app

# Install dependencies
WORKDIR /app
RUN uv sync --frozen --no-cache

# Expose the port on which the application will run
EXPOSE 5000

# Run the application
CMD [ "/app/.venv/bin/fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "5000" ]
