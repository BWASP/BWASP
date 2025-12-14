FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install -g typescript

COPY tsconfig.json ./
COPY ./src ./

RUN if [ -f .env ]; then rm .env; fi
RUN npm run clean

RUN npm run build

CMD ["npm", "run", "start"]
