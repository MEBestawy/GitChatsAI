FROM node:16-slim

WORKDIR /app

COPY src src
COPY public public
COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]