"""
Can you please get the historical price data by date for the following cryptocurrencies: cosmos, Solana, qtum, bytecoin, Gridcoin, Stratis, siacoin, nxt, factom, steem and nano
"""


# IMPORTS:

from requests import Session, RequestException
from time import perf_counter, time, sleep


start_time = perf_counter()


# CONSTANTS:

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
DATA_DIR = 'Scraped Data'  # path to data dir
SYMBOLS = ('ATOM', 'SOL', 'QTUM', 'BCN', 'GRC', 'STRAX', 'SC', 'NXT', 'FCT', 'STEEM', 'XNO')
START = 0  # default: 0 (epoch) https://en.wikipedia.org/wiki/Epoch_(computing)
STOP = int(time())  # till current date
FREQUENCY = {'Daily': 'd', 'Weekly': 'wk', 'Monthly': 'mo'}['Daily']


# MAIN:

# Session Init:
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    for i, symbol in enumerate(SYMBOLS, start=1):

        print('\n' + f'{i}) {symbol}')

        # Getting Request's Response:
        while True:
            try:
                response = session.get(url=f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}-USD?period1={START}&period2={STOP}&interval=1{FREQUENCY}&events=history&includeAdjustedClose=true')
            except RequestException as e:
                print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
                sleep(1)  # take a breath
            else:
                if response.status_code == 200:
                    break
                else:  # bad response
                    print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                    sleep(1)  # take a breath

        # print(response.headers['content-disposition'])  # debugging
        path = DATA_DIR + '\\' + response.headers['content-disposition'].rsplit('=', maxsplit=1)[-1]
        open(path, 'wb').write(response.content)
        print('Saved to:', path)


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
