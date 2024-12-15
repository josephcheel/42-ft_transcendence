#FROM node:18 AS build

#WORKDIR /app

#COPY .env ./
#COPY package*.json ./
#RUN npm install
#COPY . .

#RUN npm run build

FROM nginx:alpine

WORKDIR /app

COPY . .

RUN mkdir -p /etc/nginx/ssl/

RUN apk add --no-cache openssl vim curl iputils
#COPY --from=build /app/dist /usr/share/nginx/html
# Update package index and install prerequisites
# Install dependencies and Node.js
RUN apk add --no-cache nodejs npm
RUN npm --prefix ./ install
RUN npm --prefix ./ run build

RUN cp -rf ./dist/* /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

