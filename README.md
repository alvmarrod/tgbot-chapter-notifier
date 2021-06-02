# Manga Chapter Notifier

This bot is a Manga availability notifier, based on [mangapanda](www.mangapanda.onl) webpage.

## Deploying with Docker

1. Build your image

```
docker build .
```

2. Run a container

```
docker run -di --name bot_container <image_id>
```

3. Check inside

```
 docker exec -it <container_id> /bin/bash
```

## Dependencies

1. [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
2. [emoji](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Emoji)
3. [sqlite3](https://sqlite.org/index.html)