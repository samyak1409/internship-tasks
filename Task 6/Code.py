"""
Gridcoin: Retrieve the block level information for all the blocks using the API
(https://node.gridcoin.network/API?q=blockbyheight&height=1) and then use the transaction hash to get the transaction
level using this API (information https://node.gridcoin.network/API?q=tx&hash=[TX HASH])
"""


# Requests: ~2.5M * 2
# API Doc: https://gridcoin.network/api.html


# IMPORTS:

from requests import get as get_request
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor
from itertools import count


# CONSTANTS:

DEBUG = True  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once


# FUNCTIONS:

def get_data_from(url: str) -> dict:
    if DEBUG:
        print(url)
    data = loads(s=get_request(url=url).text)
    if DEBUG:
        print(dumps(obj=data, indent=4))
    return data


# MAIN:

def main(height: int) -> None:

    print(f'\n{height})')

    block_data = get_data_from(url=f'https://node.gridcoin.network/API?q=blockbyheight&height={height}')

    error = block_data.get('error')
    if error:
        globals()['stop'] = True
        return

    for txn_hash in block_data.get("tx"):  # list of txn hashes
        get_data_from(url=f'https://node.gridcoin.network/API?q=tx&hash={txn_hash}')


# THREADING:

stop = False
for i in count():  # infinite loop
    start = THREADS*i + 1
    with ThreadPoolExecutor() as Exec:
        Exec.map(main, range(start, start+THREADS))
    if stop or DEBUG:
        break


print('\nSUCCESS!')
