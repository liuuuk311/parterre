FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
RUN apk add --update npm

ENV LC_ALL en_US.UTF-8
ENV LANG it_IT.UTF-8
ENV LANGUAGE it_IT.UTF-8

WORKDIR /web
COPY web/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install gunicorn
COPY web .

RUN python manage.py tailwind install && python manage.py tailwind build

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
