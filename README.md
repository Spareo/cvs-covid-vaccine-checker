# cvs-covid-vaccine-checker

## Requirements
1. [pipenv](https://pypi.org/project/pipenv/)
2. python 3.8

## Configure 
Create `.env` file in root folder
Add the following 2 lines
```
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_CHAT_ID=<YOUR_TELEGRAM_CHAT_ID>
```

Install the dependencies
```
pipenv install
```

## Run
```
pipenv shell
python main.py
```