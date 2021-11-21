FROM node:17-buster
ARG DEBIAN_FRONTEND=noninteractive

# App directory
WORKDIR /usr/src/app
COPY src/. .

COPY datasets ./public/datasets

# Install NPM Dependency
RUN npm install

# Run node
CMD ["node", "bin/www"]