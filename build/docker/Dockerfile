FROM python:3.11.2-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /bot

COPY . /bot/

ENV PYTHONPATH=/bot

RUN pip3 install pipenv && pipenv install --system --deploy --ignore-pipfile

CMD "/bot/scripts/entrypoint.sh"
