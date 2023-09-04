FROM python:3.11.3

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

WORKDIR /app

COPY . /app
