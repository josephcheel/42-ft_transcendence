#FROM python:3.13.0b4-bookworm
FROM ubuntu:20.04

WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip vim clang iputils-ping

COPY /start.sh /start.sh
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
CMD ["./start.sh"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]