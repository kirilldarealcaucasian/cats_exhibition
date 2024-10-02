FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ../pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --only dev,test --without-hashes



FROM python:3.10-alpine

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /tmp/requirements.txt /project/requirements.txt

RUN apk add --no-cache bash
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY . .


