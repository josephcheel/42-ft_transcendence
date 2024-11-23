FROM node:18 AS build

WORKDIR /app

COPY .env ./
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

FROM nginx:alpine

WORKDIR /app

COPY . .

RUN mkdir -p /etc/nginx/ssl/

RUN apk add --no-cache openssl vim curl iputils

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/nginx-selfsigned.key \
  -out /etc/nginx/ssl/nginx-selfsigned.crt \
  -subj "/C=ES/ST=Barcelona/L=Barcelona/O=Transcendence/OU=Frontend/CN=localhost"

COPY /dist /usr/share/nginx/html
COPY --from=build /app/dist /usr/share/nginx/html


COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
