# syntax=docker/dockerfile:1

FROM python:3.6-slim-buster

ENV LISTEN_PORT=5000
EXPOSE 5000

WORKDIR /app
COPY PokeFlex.egg-info/requires.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
RUN python3 setup.py install
CMD [ "python3", "main.py"]