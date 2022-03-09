FROM python:3.8.12-slim

WORKDIR /app

ADD todolist /app

RUN pip install -r requirements.txt

#RUN apt update &&\
#    apt install gunicorn -y &&\
#    apt clean

ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "main:app"]