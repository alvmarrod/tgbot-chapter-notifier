FROM python:3.9.5

COPY ./ChapterNotifier/Classes/ ./app/Classes/
COPY ./ChapterNotifier/main.py ./app/
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && \
    apt-get install --no-install-recommends sqlite3 -y && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r /tmp/requirements.txt

RUN useradd -r -u 1001 -g nonroot root
USER nonroot

WORKDIR /app

ENTRYPOINT [ "python3" ]
CMD ["/app/main.py"]
