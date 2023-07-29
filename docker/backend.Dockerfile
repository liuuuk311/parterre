FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
RUN apk add --update npm

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

WORKDIR /web
COPY web/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install gunicorn
COPY web .

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
