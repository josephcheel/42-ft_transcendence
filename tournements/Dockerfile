FROM python:3.13.0b4-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y vim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["/start.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
