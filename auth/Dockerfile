FROM python:3.11-buster

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
RUN pip install --requirement requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["make", "run.dev"]
