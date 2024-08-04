FROM python:3.13.0b4-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#ensuere we still own the files
RUN chown -R 1000:1000 /app


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]