# Use the official Python base image
# NOTE: has to use slim version to avoid error when installing onnxruntime
# required by fastembed package, visit https://github.com/microsoft/onnxruntime/issues/2909
FROM python:3.11.10-slim

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"

# Install required system packages and Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unixodbc \
    odbcinst && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install the Microsoft ODBC Driver
RUN curl -sSL https://packages.microsoft.com/debian/12/prod/pool/main/m/msodbcsql17/msodbcsql17_17.10.5.1-1_amd64.deb -o msodbcsql17_17.10.5.1-1_amd64.deb && \
    ACCEPT_EULA=Y dpkg --install ./msodbcsql17_17.10.5.1-1_amd64.deb && \
    rm ./msodbcsql17_17.10.5.1-1_amd64.deb

# Set this to avoid buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Copy project package files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy the remaining application into the container
COPY . .

# Expose the port on which the application will run
EXPOSE 5000

# Default command which does nothing
# This container is used by api server and background which specify their own CMD
CMD ["tail", "-f", "/dev/null"]
