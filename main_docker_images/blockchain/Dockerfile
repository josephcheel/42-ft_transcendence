# node:alpine will be our base image to create this image
FROM node:latest
# Set the /app directory as working directory
WORKDIR /app
#Install ganache-cli globally
RUN npm install -g --unsafe-perm ganache
RUN npm install -g --unsafe-perm truffle
RUN npm install -g punycode
# Set the default command for the image
#CMD ["ganache", "-a 1", "-e 1000000", "-h", "0.0.0.0"]
CMD ["ganache", "-a 1", "-e 1000000", "--host", "0.0.0.0", "--port", "8545", "-d"]