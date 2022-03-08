# 120M


# IMPORTS:

from requests import Session
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor


# CONSTANTS:

BASE_URL = 'https://api.solscan.io'  # source: BG API from https://solscan.io/block/120000000; https://api.solscan.io/docs
DEBUG = False  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once


# MAIN:

def main(block_num: int) -> None:

    response = session.get(url=f'{BASE_URL}/block/txs?block={block_num}&offset=0&size=100000')
    print(f"\n{block_num}) {response.status_code}")

    data = loads(response.text)

    if DEBUG:
        print(BASE_URL)
        print(dumps(obj=data, indent=4))


# THREADING:

with Session() as session:

    session.stream = False

    print('\nGETTING LAST BLOCK NUMBER')
    max_block = loads(session.get(url=f'https://public-api.solscan.io/block/last?limit=1').text)[0]['currentSlot']  # https://public-api.solscan.io/docs
    print(max_block)

    for page_num in range(1, max_block, THREADS):  # start, stop, step
        with ThreadPoolExecutor() as Exec:
            Exec.map(main, range(page_num, page_num+THREADS))
        if DEBUG:
            break


print('\nSUCCESS!')
