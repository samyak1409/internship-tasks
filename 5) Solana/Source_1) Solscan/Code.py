"""
Solana: It is quite straight forward, keep parsing through the link
https://public-api.solscan.io/block/transactions?block=1&offset=0&limit=100000 until
https://public-api.solscan.io/block/transactions?block=120304941&offset=0&limit=100000
"""


# Requests: ~120M * 1
# API Doc: https://public-api.solscan.io/docs
# Default Limit: 150 requests / 30 seconds, 100k requests / day


# IMPORTS:

from requests import Session
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor
from requests_ip_rotator import ApiGateway


# CONSTANTS:

BASE_URL = 'https://public-api.solscan.io'
DEBUG = False  # (default: False)
THREADS = 1 if DEBUG else 15  # number of concurrent threads to run at once


# FUNCTIONS:

def get_data_from(url: str) -> dict:
    data = loads(s=session.get(url=url, stream=False, timeout=1).text)  # possible response codes: 200, 400, 429, 500 (https://public-api.solscan.io/docs/#/Block/get_block_transactions)
    if DEBUG:
        print(url)
        print(dumps(obj=data, indent=4))
    return data


# MAIN:

def main(block_num: int) -> None:

    print(f"\n{block_num})")

    data = get_data_from(url=f'{BASE_URL}/block/transactions?block={block_num}&limit=100000')
    # https://public-api.solscan.io/docs/#/Block/get_block_transactions

    if block_num % 75 == 0:
        print(dumps(obj=data, indent=4))


# THREADING WITH ROTATING IPs:

print()  # spacing

with ApiGateway(site=BASE_URL) as g:  # please go through: https://github.com/Ge0rg3/requests-ip-rotator

    session = Session()
    session.mount(prefix=BASE_URL, adapter=g)

    print('\nGETTING LAST BLOCK NUMBER')
    max_block = get_data_from(url=f'{BASE_URL}/block/last?limit=1')[0]['currentSlot']
    print(max_block)

    for page_num in range(1, min(300, max_block)+1, THREADS):  # start, stop, step
        with ThreadPoolExecutor() as Exec:  # https://youtu.be/IEEhzQoKtQU
            Exec.map(main, range(page_num, page_num+THREADS))
        if DEBUG:
            break

    print()  # spacing


print('\nSUCCESS!')


# Problem: Rate Limit
