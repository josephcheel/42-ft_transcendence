FROM python:3.13.0b4-bookworm

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN apt-get update -y && apt-get install -y postgresql-client

RUN chmod +x start.sh

RUN sed -i 's/\r$//g' wait_for_it.sh
RUN chmod +x wait_for_it.sh

CMD ["./start.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]