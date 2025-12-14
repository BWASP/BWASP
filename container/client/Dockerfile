FROM node:20

WORKDIR /app
COPY package*.json ./
RUN yarn install
RUN yarn global add typescript

COPY ./ /app/
RUN yarn build
RUN yarn remove-src

CMD ["yarn", "start"]
