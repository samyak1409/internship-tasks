"""
Using https://github.com/samyak1409/internship-tasks#9-always-check-for-the-hidden-api-when-web-scraping-inspect---network---xhr---name---some-get-request---response
"""


# IMPORTS:

from requests import Session, RequestException
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor
from pandas import DataFrame
from os.path import exists
from os import startfile


# CONSTANTS:

BASE_URL = 'https://explorer-api.mainnet-beta.solana.com'
DEBUG = True  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
HEADERS = {
    "authority": "explorer-api.mainnet-beta.solana.com",
    "sec-ch-ua": '"(Not(A:Brand";v="8", "Chromium";v="98", "Google Chrome";v="98"',
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "content-type": "application/json",
    "accept": "*/*",
    "origin": "https://explorer.solana.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://explorer.solana.com",
    "accept-language": "en-US,en;q=0.9"
}
START = 1
TOTAL = 1_000_000  # 1M blocks to scrape
while True:
    STOP = START + TOTAL  # 1_000_001
    EXCEL = f'Scraped Data\\{START}-{STOP-1}.xlsx'
    if not exists(EXCEL):
        break
    START += TOTAL


# MAIN:

def main(block: int) -> None:

    # Getting Request's Response:
    payload = {
        "method": "getConfirmedBlock",
        "jsonrpc": "2.0",
        "params": [block, {"commitment": "confirmed"}],
        "id": ""
    }
    while True:
        try:
            response = session.post(url=BASE_URL, json=payload)
        except RequestException as e:
            if DEBUG:
                print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
        else:
            if response.status_code == 200:
                break
            else:  # bad response
                if DEBUG:
                    print(f'{response.status_code}: {response.reason} TRYING AGAIN...')

    data = loads(s=response.text)['result']
    print(f"\n{block}) Data Items: {len(data)}; Transactions: {len(data['transactions'])}")

    data['blockHeight'] = block  # block height was empty for some reason

    if DEBUG:
        print(dumps(obj=data, indent=4))

    data_list.append(data)


# SESSION INIT:

with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    data_list = []

    # THREADING:
    for page_num in range(START, STOP, THREADS):  # start, stop, step
        with ThreadPoolExecutor() as Exec:
            Exec.map(main, range(page_num, page_num+THREADS))
        if DEBUG:
            break

    DataFrame(data=data_list).to_excel(EXCEL, index=False)  # saving data to excel


startfile(EXCEL)
print('\nSUCCESS!')


# Problem: Block Time N/A
