"""
Ok for the next task we need to get trading data from this source: https://www.cryptodatadownload.com/data/
If you scroll to the end to this page you will find exchanges listed here
I need data from all of these exchanges for all currency pair. The data will be both daily and hourly. I need only daily data
"""


# IMPORTS:

from time import perf_counter, sleep
from requests import Session, RequestException, Response
from bs4 import BeautifulSoup
from os import mkdir, chdir


start_time = perf_counter()


# ATTRIBUTES:

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
BASE_URL = 'https://www.cryptodatadownload.com/data'
API = 'https://api.cryptodatadownload.com'
DEBUG = False  # default: False
DATA_DIR = 'Scraped Data'


# FUNCTIONS:

def get_response(url: str) -> Response:
    """Gets Request's Response"""
    while True:
        try:
            response = session.get(url=url)
        except RequestException as e:
            print(f'{type(e).__name__}: ' + e.__doc__.split('\n')[0] + '; ' + 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:
            if response.status_code == 200:
                return response
            if response.status_code == 404:  # not found
                break  # returns None
            # else: bad response
            print(f'{response.status_code}: {response.reason}; TRYING AGAIN...')
            sleep(1)  # take a breath


# MAIN:

# Session Init:
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    try:
        mkdir(DATA_DIR)
    except FileExistsError:
        pass
    chdir(DATA_DIR)

    # Step 1:
    print('\n' + 'Getting Exchanges...')  # spacing
    soup = BeautifulSoup(markup=get_response(url=BASE_URL).text, features='html.parser')
    # print(soup.prettify())  # debugging
    exchanges = set()
    for regions in soup.find(name='ul', class_='rd-navbar-dropdown').find_all(name='li', recursive=False):
        exchanges_region_wise = regions.find(name='ul', class_='rd-navbar-dropdown')
        if exchanges_region_wise is not None:
            for exchange in exchanges_region_wise.find_all(name='li', recursive=False):
                # print(exchange.prettify())  # debugging
                exchanges.add(exchange.text)
    print(exchanges, '\n')

    print(f'Getting Exchanges already downloaded using API ({API})...')
    exchanges_from_api = set(get_response(url=f'{API}/?format=openapi').json()['definitions'].keys())
    print(exchanges_from_api)

    for exchange_num, exchange in enumerate(filter(lambda xchange: xchange not in exchanges_from_api, exchanges), start=1):

        try:
            mkdir(exchange)
        except FileExistsError:
            pass

        # Step 2) Getting direct download links of all the symbols of an exchange:
        data_url = f'{BASE_URL}/{exchange.lower()}'
        print('\n' + f'{exchange_num}) {exchange}: {data_url}')


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
