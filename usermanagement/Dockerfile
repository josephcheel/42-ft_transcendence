FROM eavedillo/transcendence:latest

WORKDIR /app

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]