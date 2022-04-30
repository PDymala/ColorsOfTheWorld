# Python image to use.
FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]

#ENTRYPOINT [ "python" "manage.py"]
#CMD [ "runserver", "0.0.0.0:8080" ]