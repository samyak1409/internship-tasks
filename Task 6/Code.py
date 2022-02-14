"""
Gridcoin: Retrieve the block level information for all the blocks using the API
(https://node.gridcoin.network/API?q=blockbyheight&height=1) and then use the transaction hash to get the transaction
level using this API (information https://node.gridcoin.network/API?q=tx&hash=[TX HASH])
"""


# Requests: ~2.5M
# API Doc: https://gridcoin.network/api.html


# IMPORTS:

from requests import get as get_request
from json import loads, dumps


# FUNCTIONS:

def get_data_from(url: str) -> dict:
    print(url)
    data = loads(s=get_request(url=url).text)
    print(dumps(obj=data, indent=4))
    return data


# MAIN:

START = 1

try:
    stop = int(input('\nHOW MANY?: '))
except ValueError as e:
    raise SystemExit(e)

for height in range(START, START+stop):

    print(f'\n{height})')

    block_data = get_data_from(url=f'https://node.gridcoin.network/API?q=blockbyheight&height={height}')

    error = block_data.get('error')
    if error:
        break

    for txn_hash in block_data.get("tx"):  # list of txn hashes
        get_data_from(url=f'https://node.gridcoin.network/API?q=tx&hash={txn_hash}')


print('\nSUCCESS!')
