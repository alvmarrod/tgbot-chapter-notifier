# [Telegram Bot] Chapter Notifier

<p align="center">
  <img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/alvmarrod/tgbot-chapter-notifier">
  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue">
  <img alt="Dynamic JSON Badge" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Falvmarrod%2Ftgbot-chapter-notifier%2Frefs%2Fheads%2Fmaster%2Fpublish_data.json&query=tests.coverage&label=Test%20Coverage">
  <img alt="GitHub License" src="https://img.shields.io/github/license/alvmarrod/tgbot-chapter-notifier">
</p>

## 1. Overview

This `Chapter Notifier` is a telegram bot aimed to search and then notify to the suscribed users the availability of a new manga chapter, based on [mangapanda](http://mangapanda.onl) webpage.

Due to the implementation being layered and generic enough, it is easily adaptable to other projects that aim for the same working flow: `[query a source] -> [process] -> [store in database] -> [notify]`

## 2. Features

The app has a behaviour that is configurable ...

## 3. Project Structure

The project is organized accordingly to layered architecture principles, which clear separation between `infrastructure`, `domain` and `app` layers.

## 4. Execution

To execute the bot, provide a valid `.env` file at `src` directory as `src/.env` with the following variables. Note that `BOT_NAME` and `ADMIN_USERNAME` are not in use so far, so their value is not important.

```properties
TB_CHAPTER_NOTIFIER_API_ID=
TB_CHAPTER_NOTIFIER_API_HASH=
TB_CHAPTER_NOTIFIER_BOT_TOKEN=

BOT_NAME=
ADMIN_USERNAME=
DATABASE_FILEPATH=data/roger_db.db
```

Then:

```bash
make run
```

## 5. Deploying with Docker

You can deploy it directly either using `docker-compose.yaml` provided file or `make docker-deploy`. In case of the first

1. Build your image

```bash
make docker-build
```

2. Run a container

```bash
docker run -d --env-file ./src/.env -v $(pwd)/app/data:/app/data tgbot-chaptnotifier:1.0.0
```

## Testing

You can run all the unitary tests for the project using `make test`. As result, you will also get the coverage result in [coverage_percentage.txt](./coverage_percentage.txt).

## FAQ

- Q: Should the project run correctly (and its tests) just after `git clone`?

> No, remember this is a telegram bot. `pyrogram client` initialization has not been mocked, so you will need to setup your `.env` file to provide the necessary environment variables.

- Q: Does the service works out of the box as docker container?

> A: Yes.

- Q: I have issues running the container out of the box due to the database file. Why?

> The container is configured to run as non-root user. Due to this configuration, you need your `/app/` folder to be configured to belong to the group with id `4444` and the folder and its subdirectories need to have the same group as owner. This is necessary for the bot to be able to generate the database file.

## Dependencies

1. [pyrofork](https://github.com/Mayuri-Chan/pyrofork)
2. [emoji](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Emoji)
3. [sqlite3](https://sqlite.org/index.html)
4. [python-dotenv](https://github.com/theskumar/python-dotenv)
5. [apscheduler](https://github.com/agronholm/apscheduler)
6. [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

## Contributing

Contributions are welcome! Please submit issues or pull requests with your changes. Make sure to follow the existing code style and add tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
