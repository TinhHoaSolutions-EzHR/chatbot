# Use the official Python base image
# NOTE: has to use slim version to avoid error when installing onnxruntime
# required by fastembed package, visit https://github.com/microsoft/onnxruntime/issues/2909
# also, for odbc to work with SQL Server
FROM python:3.11.10-slim-bookworm

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"
LABEL org.opencontainers.image.descripiton "Docker image for backend api_server"

# Install required system packages and Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl=7.88.1-10+deb12u8 \
  unixodbc=2.3.11-2+deb12u1 \
  odbcinst=2.3.11-2+deb12u1 && \
  curl -sSL https://packages.microsoft.com/debian/12/prod/pool/main/m/msodbcsql17/msodbcsql17_17.10.6.1-1_amd64.deb -o msodbcsql17_17.10.6.1-1_amd64.deb && \
  ACCEPT_EULA=Y dpkg --install ./msodbcsql17_17.10.6.1-1_amd64.deb && \
  rm ./msodbcsql17_17.10.6.1-1_amd64.deb && \
  apt-get clean && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/*

# Set this to avoid buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container, including uv.lock
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN uv sync --frozen --no-cache

# Expose the port on which the application will run
EXPOSE 5000

# Default command which does nothing
# This container is used by api server and background which specify their own CMD
CMD ["tail", "-f", "/dev/null"]
