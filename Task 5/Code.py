"""
Solana: It is quite straight forward, keep parsing through the link
https://public-api.solscan.io/block/transactions?block=1&offset=0&limit=100000 until
https://public-api.solscan.io/block/transactions?block=120304941&offset=0&limit=100000
"""


# IMPORTS:

from requests import get as get_request
from json import loads, dumps


# MAIN:

START = 1

try:
    stop = int(input('\nHOW MANY?: '))
except ValueError as e:
    raise SystemExit(e)

for block_num in range(START, START+stop):

    url = f'https://public-api.solscan.io/block/transactions?block={block_num}&offset=0&limit=100000'
    print(f'\n{block_num}) {url}')

    data_dict = loads(s=get_request(url=url).text)

    len_ = len(data_dict)
    print('LEN:', len_)
    if not len_:
        print('MAX HEIGHT REACHED')
        break

    print(dumps(obj=data_dict, indent=4))
