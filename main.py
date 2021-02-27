import urllib.request, json, logging, sys, os, requests, schedule, datetime, time

from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint

def get_state_abbreviation(long_name):
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands':'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    return us_state_abbrev[long_name]

def get_covid_info_url_for_sate(long_name):
    state_abbrev = get_state_abbreviation(long_name)
    return f"https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.{state_abbrev}.json?vaccineinfo"


def create_logger():
    logFormatter = logging.Formatter("%(asctime)s %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel("INFO")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    return rootLogger


def send_telegram(logger, message):
    send_url = 'https://api.telegram.org/bot' + os.getenv("TELEGRAM_BOT_TOKEN") + '/sendMessage?chat_id=' + os.getenv("TELEGRAM_CHAT_ID") + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_url)
    logger.info(response.json())


def run(cities, state, logger):
    vaccine_statuses = None

    cities = [c.upper() for c in cities]
    state_abbrev = get_state_abbreviation(state)
    cvs_url = get_covid_info_url_for_sate(state)
    logger.info(f"Retrieving CVS vaccine info from {cvs_url}")

    with urllib.request.urlopen(cvs_url) as url:
        data = json.loads(url.read().decode())

        if (data is None):
            logger.error("Failed to retrieve state vaccine information, please make sure your state is available on the CVS vaccine website.")
            sys.exit(1)

        vaccine_statuses = data['responsePayloadData']['data'][state_abbrev.upper()]

    to_process = len(cities)
    for response_item in vaccine_statuses:
        city = response_item['city']
        status = response_item['status']
        if city in cities:
            to_process -= 1
            logger.info(f"{city} is {status}")

            if status.lower() == "available":
                send_telegram(logger, f"****Sign up for COVID vaccine in {city} at https://www.cvs.com/immunizations/covid-19-vaccine****")

        if to_process == 0:
            logger.info("Finished checking requested cities, going to sleep.")
            break


if __name__ == "__main__":
    load_dotenv()
    is_first_run = True

    state = "Texas"
    cities = ["Plano", "Richardson"]

    logger = create_logger()
    schedule.every(15).minutes.do(run)

    while True:
        if is_first_run:
            run(cities, state, logger)
            is_first_run = False
        else:
            next_run = schedule.next_run()
            next_run_diff = next_run - datetime.now()
            next_run_minutes = round(next_run_diff.total_seconds() / 60)
            logger.info("Next run in {} minutes".format(next_run_minutes))

            schedule.run_pending()

            # Sleep until the next run + some extra time so when the loop 
            time.sleep(next_run_minutes * 60 + 5)

    