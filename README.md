# Top Décollage

Welcome to Top Décollage!

This project is a Telegram Bot implemented using BERNARD's platform. 
Please refer to [BERNARD's documentation](https://github.com/BernardFW/bernard) for further details.


## What is this all about?

The purpose of this project is to build a Telegram bot that will figure out the exact lift off time from a rocket launch video.

The bot will prompt a user showing different frames extracted from a Falcon Heavy launch video. It will then use a bisection algorithm to narrow down the posibilities until the first frame where the rocket is launched (the T0) is reached. 

Tipically in doesn't take more than 17 rounds (prompts) to finish.


## Live Demo

Feel free to try this bot in [https://t.me/TopDecollage](https://t.me/TopDecollageBot)


## Dependencies

- [BERNARD](https://github.com/BernardFW/bernard)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

.. For a comprehensive list of Python dependencies checkout `poetry.lock` and `requirements.txt` from [BERNARD's project](https://github.com/BernardFW/bernard).


## Configuration

Copy `credentials/credentials-template.env` as `credentials/credentials.env` and fill:

- *WEBVIEW_SECRET_KEY*: Just a secret for the app to sign communications.
- *TELEGRAM_TOKEN*: Your bot token provided by @BotFather.

Also, you need to edit `env/prod.env` file for your needs.
- *BERNARD_BASE_URL*: The public url or your bot.
- *DOCKER_REGISTRY_URL*: A Docker container registry to push your image.


## Build

Build operations are managed through a makefile for convinience.

In order to build the project from the sources, follow these steps:

1. Run `make build` to build the image.
2. Run `make tag` to tag image as VERSION.
3. Run `make push` to push image to upload the image to the container registry.

NOTE: This project is version managed. See [Versioning](#versioning) for detailed info.


## Installation

This project is designed to be run inside Docker but it can be easily adapted to be run elsewhere. 

In order to deploy the project with Docker follow this steps:
1. Copy `docker-compose.yml` to the target server.
2. Also copy `credentials/credentials.env` and `env/prod.env`
3. Run `docker-compose up`


## Development environment

1. Clone the repository: `git clone https://github.com/tu-usuario/tu-proyecto.git`
2. Create a virtual environment (opcional): `python3 -m venv venv`
4. Activate your virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Launch the application: `python manage.py run`

You need a Linux-based machine in order to nativelly run the project with `python manage.py run` due to `aiohttp` limitations.

In case you can't install the dependencies you can use `docker-compose.dev.yml`. This tuned version of docker-compose.yml will build your sources on-the-fly and fetch local env files accordingly.


## Translation

Localization files live under i18n folder.


## Versioning

This project folows [Semantic Versioning](https://semver.org).

Please note that:

- Version is kept inside VERSION file.
- Docker image is tagged using VERSION content.
- `docker-compose.yml` references VERSION. 

## Motivation

This project has been coded as a test for WITH Madrid.


## Licensing

This code is licensed under AGPL v3+ like its parent project BERNARD.