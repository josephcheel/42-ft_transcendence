# Base image
FROM node:latest

# Create app directory
WORKDIR /app

# Install dependencies first by copying only the package.json and package-lock.json
# This ensures that npm install is re-run only when package files change
COPY ./package*.json ./
COPY ./ecosystem.config.cjs ./

# Install app dependencies
RUN npm install

# Copy the entire app source code after installing dependencies
COPY app/backend.js .

# Install node server daemon
RUN npm install pm2 -g

#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#  -keyout /app/selfsigned.key \
#  -out /app/selfsigned.crt \
#  -subj "/C=ES/ST=Barcelona/L=Barcelona/O=Transcendence/OU=Pong-WS-Server/CN="

# Expose port 3000
EXPOSE 4000

# Start Nginx
CMD ["pm2-runtime", "start", "ecosystem.config.cjs"]
