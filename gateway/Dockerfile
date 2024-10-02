FROM python:3.13.0b4-bookworm

WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip vim curl iputils-ping

COPY /start.sh /start.sh
COPY /test.sh /test.sh
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
CMD ["./start.sh"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]