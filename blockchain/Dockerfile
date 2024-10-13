# node:alpine will be our base image to create this image
FROM node:14
# Set the /app directory as working directory
WORKDIR /app
#Install ganache-cli globally
RUN npm install -g ganache
RUN npm install -g truffle
RUN npm install -g punycode
# Set the default command for the image
#CMD ["ganache", "-a 1", "-e 1000000", "-h", "0.0.0.0"]
CMD ["ganache", "--host", "0.0.0.0", "--port", "8545"]
