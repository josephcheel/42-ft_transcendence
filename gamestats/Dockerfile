FROM python:3.13.0b4-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#ensure we still own the files
RUN chown -R 1000:1000 /app

CMD ["/start.sh"]