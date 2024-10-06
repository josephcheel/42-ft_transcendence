FROM python:3.13.0b4-bookworm

WORKDIR /app
RUN apt-get update && apt-get install -y python3-pip vim curl iputils-ping

COPY . .

RUN pip install -r requirements.txt


RUN chmod +x start.sh
RUN chown root:root test.sh
RUN chmod +x test.sh

EXPOSE 8000

#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
CMD ["./start.sh"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]