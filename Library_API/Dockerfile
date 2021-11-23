

FROM python:3.7.12-slim-buster as builder

WORKDIR /usr/src/app

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
  && apt-get -y install --no-install-recommends gcc netcat \
    postgresql libpq-dev python3-dev musl-dev \
  && apt-get clean

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

## FINAL

FROM python:3.7.12-slim-buster

RUN useradd --create-home library_backend
WORKDIR /home/library_backend
RUN mkdir /home/library_backend/static
RUN mkdir /home/library_backend/media

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . .

COPY ./entrypoint.sh /home/library_backend/entrypoint.sh
RUN chmod +x /home/library_backend/entrypoint.sh

RUN chown -R library_backend /home/library_backend

RUN python manage.py collectstatic --noinput

USER library_backend

ENTRYPOINT ["/home/library_backend/entrypoint.sh"]

CMD gunicorn Library_API.wsgi:application --bind 0.0.0.0:$PORT