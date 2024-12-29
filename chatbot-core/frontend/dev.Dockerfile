FROM node:20-alpine AS base

FROM base AS builder

RUN apk add --no-cache libc6-compat

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .


CMD [ "npm", "run", "dev" ]
