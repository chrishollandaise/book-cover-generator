FROM node:18-alpine
WORKDIR /webapp
COPY package.json package-lock.json ./
RUN npm install --silent
COPY . ./
EXPOSE 8080