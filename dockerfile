FROM python:3.11.9

LABEL team="Octowit"

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /networking-project/

COPY ./requirements.txt /networking-project/requirements.txt

RUN pip install -r /networking-project/requirements.txt

WORKDIR /networking-project/
COPY ./networking /networking-project/backend
