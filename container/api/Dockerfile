FROM node:20

WORKDIR /app

# package.json 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# TypeScript 소스 복사
COPY tsconfig.json ./
COPY ./src ./src

# TypeScript 컴파일
RUN npx tsc

# 환경변수 설정
ENV NODE_ENV=production

CMD ["npm", "run", "start"]
