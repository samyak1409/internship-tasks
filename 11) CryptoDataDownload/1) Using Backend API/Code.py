"""
Ok for the next task we need to get trading data from this source: https://www.cryptodatadownload.com/data/
If you scroll to the end to this page you will find exchanges listed here
I need data from all of these exchanges for all currency pair. The data will be both daily and hourly. I need only daily data
"""


# IMPORTS:

from time import perf_counter, sleep
from requests import Session, RequestException, Response
# from json import dumps  # debugging
from os import mkdir, chdir


start_time = perf_counter()


# ATTRIBUTES:

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
BASE_URL = 'https://api.cryptodatadownload.com'
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
    json_data = get_response(url=f'{BASE_URL}/?format=openapi').json()
    # print(dumps(obj=json_data, indent=4))  # debugging
    exchanges = list(json_data['definitions'].keys())
    exchanges.append('Cex')  # not listed on API page, but data available on API!
    print(exchanges)

    for exchange_num, exchange in enumerate(exchanges, start=1):

        try:
            mkdir(exchange)
        except FileExistsError:
            pass

        # Step 2) Getting direct download links of all the symbols of an exchange:
        data_url = f'{BASE_URL}/v1/data/ohlc/{exchange.lower()}/available?format=json'
        print('\n' + f'{exchange_num}) {exchange}: {data_url}')

        json_data = get_response(url=data_url).json()
        # print(dumps(obj=json_data, indent=4))  # debugging

        direct_download_links = {}  # symbol: direct_download_link
        try:
            for data_dict in json_data['data']:  # https://api.cryptodatadownload.com/v1/data/ohlc/bitstamp/available?format=json
                # print(data_dict)  # debugging
                if data_dict['timeframe'] == 'day':
                    direct_download_links[data_dict['symbol']] = data_dict['file']
        except TypeError:  # sometimes the data is faulty, see: https://api.cryptodatadownload.com/v1/data/ohlc/binance/available?format=json
            for symbol in json_data:
                # print(symbol)  # debugging
                direct_download_links[symbol] = f'https://www.cryptodatadownload.com/cdd/{exchange}_{symbol.replace("/", "")}_d.csv'

        # Step 3) Downloading:
        for symbol_num, (symbol, direct_download_link) in enumerate(direct_download_links.items(), start=1):

            print(f'{exchange_num}.{symbol_num}) {symbol}: {direct_download_link}')

            if not DEBUG:
                try:
                    data = get_response(url=direct_download_link).content
                except AttributeError:  # when get_response returns None
                    print('The requested resource was not found on this server.')
                else:
                    open(f'{exchange}\\{symbol.replace("/", " ")}.csv', 'wb').write(data)


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
