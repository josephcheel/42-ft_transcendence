FROM eavedillo/transcendence:latest

COPY . .

RUN chmod +x start.sh
RUN chown root:root test.sh
RUN chmod +x test.sh

RUN chmod +x start.sh
RUN chown root:root test.sh

EXPOSE 8000

#ENTRYPOINT [ "bash", "-c", "while true; do sleep 3306; done"]
CMD ["./start.sh"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]