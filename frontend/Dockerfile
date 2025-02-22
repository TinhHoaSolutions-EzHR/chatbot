# Stage 1: Build the app
FROM node:22.12.0-alpine AS build

WORKDIR /app

# Copy package.json and yarn.lock to /app
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile && \
  yarn cache clean

# Copy the rest of the files to /app
COPY . .

# Build the app
RUN yarn build

# Stage 2: Serve the app with nginx
FROM nginx:1.23.4-alpine AS serve

# Set label to push to GitHub Container Registry
LABEL org.opencontainers.image.source "https://github.com/TinhHoaSolutions-EzHR/chatbot"
LABEL org.opencontainers.image.descripiton "Docker image for frontend web-server"

# Copy the build output to replace the default nginx contents
COPY --from=build /app/out /var/www/out

EXPOSE 80

# Tail to /dev/null to keep the container running
CMD ["tail", "-f", "/dev/null"]
