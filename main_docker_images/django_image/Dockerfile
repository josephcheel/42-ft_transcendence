FROM python:3.13.0b4-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# configure time zone Madrid
RUN apt-get update 
RUN apt install -y systemd  
#RUN timedatectl set-timezone Europe/Madrid 
RUN ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime
RUN echo "Europe/Madrid" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git
  # install 
  # cleaning up unused files
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
  
# Requirements are installed here to ensure they will be cached.
COPY . .
#RUN pwd
RUN pip install -r requirements.txt

#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
