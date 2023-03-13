FROM python:3.11.2-slim-buster

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0
ENV PORT=8080

RUN apt-get update  \
    && apt-get -y install netcat gcc postgresql  \
    && apt-get clean \

RUN pip install --upgrade pip
COPY /project/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install "uvicorn[standard]==0.20.0"

COPY /project .

RUN chown -R app:app $APP_HOME

USER app

CMD gunicorn --bind 0.0.0.0:$PORT app.main:app -k uvicorn.workers.UvicornWorker