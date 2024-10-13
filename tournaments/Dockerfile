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
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get update -y && apt-get install -y postgresql-client

WORKDIR /app

# Requirements are installed here to ensure they will be cached.
COPY ./start.sh /start.sh
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

CMD ["/start.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
