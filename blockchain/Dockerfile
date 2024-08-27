FROM ubuntu:20.04

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
	wget \ 
	p7zip-full \
	fuse libfuse2 \
	&& rm -rf /var/lib/apt/lists/*

# Copiar el archivo AppImage
WORKDIR /tmp/
RUN wget https://github.com/trufflesuite/ganache-ui/releases/download/v2.7.1/ganache-2.7.1-linux-x86_64.AppImage

# Dar permisos de ejecución
RUN chmod +x /tmp/ganache-2.7.1-linux-x86_64.AppImage
COPY /script.sh /tmp/script.sh

# Exponer el puerto 8545 para Ganache
EXPOSE 8545

# Comando de inicio
#CMD ["/usr/local/bin/ganache.AppImage", "--no-sandbox"]
ENTRYPOINT ["bash", "/tmp/script.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]