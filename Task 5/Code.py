"""
Solana: It is quite straight forward, keep parsing through the link
https://public-api.solscan.io/block/transactions?block=1&offset=0&limit=100000 until
https://public-api.solscan.io/block/transactions?block=120304941&offset=0&limit=100000
"""


# Requests: ~120M * 1
# API Doc: https://public-api.solscan.io/docs/


# IMPORTS:

from requests import get as get_request
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor


# CONSTANTS:

DEBUG = True  # (default: False)
THREADS = 1 if DEBUG else 150  # number of concurrent threads to run at once


# FUNCTIONS:

def get_data_from(url: str) -> dict:
    data = loads(s=get_request(url=url).text)
    if DEBUG:
        print(url)
        print(dumps(obj=data, indent=4))
    return data


# MAIN:

def main(block_num: int) -> None:

    print(f"\n{block_num})")

    get_data_from(url=f'https://public-api.solscan.io/block/transactions?block={block_num}')


# THREADING:

if DEBUG:
    print('\nGETTING LAST BLOCK NUMBER')  # spacing
for page_num in range(1, get_data_from(url=f'https://public-api.solscan.io/block/last?limit=1')[0]['currentSlot']+1, THREADS):  # start, stop, step
    with ThreadPoolExecutor() as Exec:
        Exec.map(main, range(page_num, page_num+THREADS))
    if DEBUG:
        break


print('\nSUCCESS!')
