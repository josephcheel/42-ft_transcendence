FROM python:3.13.0b4-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update -y && apt-get install -y postgresql-client

COPY . .

CMD ["./start.sh"]