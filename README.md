# cvs-covid-vaccine-checker

## Requirements
1. [pipenv](https://pypi.org/project/pipenv/)
2. python 3.8

## Telegram 
1. Create a bot in telegram ([instructions](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot))
2. Save the token you get back from the @BotFather
2. Create a group chat in telegram 
3. Add the bot to the group chat ([instructions](https://stackoverflow.com/questions/37338101/how-to-add-a-bot-to-a-telegram-group))
4. Get the group chat ID ([instructions](https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659))

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

## Run Example
```
pipenv shell
python main.py --state Virginia --city Abingdon --city Dublin --interval 15
```

**NOTE:** Your cities and state must come from the list of available cities and states found [here](https://www.cvs.com/immunizations/covid-19-vaccine)

## Help
```
Usage: main.py [OPTIONS]

Options:
  --state TEXT        The name of the state to check availability in
                      [required]

  -c, --city TEXT     The name of the city to check availability for in your
                      state  [required]

  --interval INTEGER  The internval at which the availability status will be
                      checked (minutes)

  --help              Show this message and exit.
```