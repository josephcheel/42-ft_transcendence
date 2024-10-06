FROM python:3.13.0b4-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


#COPY . .


RUN apt-get update \
	&& apt-get install -y vim sqlite3 sudo \
	# dependencies for building Python packages
	&& apt-get install -y build-essential \
	# psycopg2 dependencies
	&& apt-get install -y libpq-dev \
	# Translations dependencies
	&& apt-get install -y gettext \
	# Additional dependencies
	&& apt-get install -y git \
	# cleaning up unused files
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/*
	
WORKDIR /app

# Requirements are installed here to ensure they will be cached.
COPY ./start.sh /start.sh
COPY ./requirements.txt /requirements.txt
COPY ./wait_for_it.sh /wait_for_it.sh
RUN pip install -r /requirements.txt

RUN sed -i 's/\r$//g' /wait_for_it.sh 
RUN chmod +x /wait_for_it.sh 
RUN chmod +x /start.sh

CMD ["/start.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
