# services/<service>/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

# Install dockerize binary
RUN apk add --no-cache wget \
  && wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-alpine-linux-amd64-v0.6.1.tar.gz \
  && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-v0.6.1.tar.gz \
  && rm dockerize-alpine-linux-amd64-v0.6.1.tar.gz

# Expose only for orders
EXPOSE 5002

CMD ["node", "server.js"]
