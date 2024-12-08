# Use the official Python base image
# NOTE: has to use slim version to avoid error when installing onnxruntime
# required by fastembed package, visit https://github.com/microsoft/onnxruntime/issues/2909
# also, for odbc to work with SQL Server
FROM python:3.11.10-slim-bookworm

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"
LABEL org.opencontainers.image.descripiton "Docker image for backend api_server"

# Set this to avoid buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install required system packages, Microsoft ODBC Driver for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl=7.88.1-10+deb12u8 \
  ca-certificates=20230311 \
  unixodbc=2.3.11-2+deb12u1 \
  odbcinst=2.3.11-2+deb12u1 && \
  curl -sSL https://packages.microsoft.com/debian/12/prod/pool/main/m/msodbcsql17/msodbcsql17_17.10.6.1-1_amd64.deb -o msodbcsql17_17.10.6.1-1_amd64.deb && \
  ACCEPT_EULA=Y dpkg --install ./msodbcsql17_17.10.6.1-1_amd64.deb && \
  rm ./msodbcsql17_17.10.6.1-1_amd64.deb && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get clean

# Set the working directory in the container
WORKDIR /app

# Install uv and dependencies
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/
COPY pyproject.toml /app
COPY uv.lock /app
RUN uv sync --no-dev --frozen --no-cache --verbose

# Cleanup for CVEs and size reduction
# https://github.com/tornadoweb/tornado/issues/3107
# xserver-common and xvfb included by playwright installation but not needed after
# perl-base is part of the base Python Debian image but not needed for Danswer functionality
# perl-base could only be removed with --allow-remove-essential
RUN apt-get update && \
  apt-get remove -y --allow-remove-essential \
  perl-base \
  xserver-common \
  xvfb \
  cmake \
  libldap-2.5-0 \
  libxmlsec1-dev \
  pkg-config \
  gcc && \
  apt-get install -y libxmlsec1-openssl && \
  apt-get autoremove -y && \
  rm -rf /var/lib/apt/lists/* && \
  rm -f /usr/local/lib/python3.11/site-packages/tornado/test/test.key

# Copy the application into the container, including uv.lock
COPY . /app

# Expose the port on which the application will run
ENV PYTHONPATH=/app
EXPOSE 5000

# Default command which does nothing
# This container is used by api server and background which specify their own CMD
CMD ["tail", "-f", "/dev/null"]
