FROM python:3.12-slim

RUN apt-get update && \
    apt-get install sqlite3 -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r /tmp/requirements.txt

RUN groupadd -g 4444 bots \
    && useradd -u 1001 -g bots nonroot
RUN mkdir -p /app

COPY ./src/app/ /app/app/
COPY ./src/domain/ /app/domain/
COPY ./src/infrastructure/ /app/infrastructure/

COPY ./src/*.py /app/
COPY ./src/version.txt /app/

RUN chown -R 1001:4444 /app
USER 1001:4444
WORKDIR /app
CMD ["python", "main.py"]
