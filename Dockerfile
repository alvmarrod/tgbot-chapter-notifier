FROM python:3.9.5

RUN apt-get update && \
    apt-get install sqlite3 -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r /tmp/requirements.txt

RUN useradd -r -u 1001 -g root nonroot

COPY ./ChapterNotifier/Classes/ /app/Classes/
COPY ./ChapterNotifier/main.py /app/
COPY PrivateData /PrivateData

RUN chown nonroot -R /app
WORKDIR /app

USER nonroot
ENTRYPOINT [ "python3" ]
CMD ["/app/main.py"]
