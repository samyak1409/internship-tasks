"""
Ok for the next task we need to get trading data from this source: https://www.cryptodatadownload.com/data/
If you scroll to the end to this page you will find exchanges listed here
I need data from all of these exchanges for all currency pair. The data will be both daily and hourly. I need only daily data
"""


# IMPORTS:

from time import perf_counter, sleep
from requests import Session, RequestException
from bs4 import BeautifulSoup


start_time = perf_counter()


# ATTRIBUTES:

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
BASE_URL = 'https://www.cryptodatadownload.com/data'


# MAIN:

# Session Init:
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    # Getting Request's Response:
    while True:
        try:
            response = session.get(url=BASE_URL)
        except RequestException as e:
            print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:
            if response.status_code == 200:
                break
            else:  # bad response
                print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                sleep(1)  # take a breath

    soup = BeautifulSoup(markup=response.text, features='html.parser')
    print(soup.prettify())  # debugging


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
