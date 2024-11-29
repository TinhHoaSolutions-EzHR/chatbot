# Use the official Python base image
# NOTE: has to use slim version to avoid error when installing onnxruntime
# required by fastembed package, visit https://github.com/microsoft/onnxruntime/issues/2909
FROM python:3.11.10-slim

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"

# Set this to avoid buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container, including uv.lock
COPY . /app

# Install dependencies
WORKDIR /app
RUN uv sync --frozen --no-cache

# Expose the port on which the application will run
EXPOSE 5000

# Default command which does nothing
# This container is used by api server and background which specify their own CMD
CMD ["tail", "-f", "/dev/null"]
