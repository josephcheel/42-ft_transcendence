# node:alpine will be our base image to create this image
FROM eavedillo/blockchain:latest
# Set the /app directory as working directory
WORKDIR /app
CMD ["ganache", "-a 1", "-e 100000000", "--host", "0.0.0.0", "--port", "8545", "-d", "--verbose" "--debug"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
