FROM python:3.7.12-slim-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install --no-install-recommends gcc netcat \
    postgresql libpq-dev python3-dev musl-dev \
  && apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN useradd --create-home library_backend
WORKDIR /home/library_backend

COPY ./entrypoint.sh /home/library_backend/entrypoint.sh
RUN chmod +x /home/library_backend/entrypoint.sh

COPY . .

USER library_backend

ENTRYPOINT ["/home/library_backend/entrypoint.sh"]