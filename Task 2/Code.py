"""
For the next task can you pull up the transactions' data for Cosmos. You can use their API to do so.
The information is documented here: https://v1.cosmos.network/rpc/v0.41.4

Looks like the lowest height of the block is 5200791.
With proper sleep times you just need a for loop to make calls to this (https://api.cosmos.network/blocks/5200791)
where the block number will be increasing by 1 in next API calls.
You need to read the json and keep adding to your dataframe and then write in a CSV.
"""


# IMPORTS:

from requests import get as get_request
from json import loads, dumps
from pandas import DataFrame
from os.path import exists
from sys import stdout


# ATTRIBUTES:

START = 5200791
CSV_DIR = 'Scraped Data (CSVs)'
BASE_URL = 'https://api.cosmos.network/blocks'
JSON_TXT = 'Scraped Data (JSON).txt'


# MAIN:

try:
    blocks = int(input('\nHow many?: '))
except ValueError:
    raise SystemExit('\nERROR: EMPTY OR NON-NUMERIC INPUT')

height = START

while height != START+blocks:

    csv = f'{CSV_DIR}\\{height}.csv'

    if not exists(path=csv):  # if not already scraped

        data_dict = loads(s=get_request(url=f'{BASE_URL}/{height}').text)

        with open(file=JSON_TXT, mode='a') as f:
            print()  # spacing
            for obj in (stdout, f):
                print(f'Block #{height}', file=obj)
            # print(dumps(obj=data_dict, indent=4))  # debugging
            del data_dict['block']['last_commit']['signatures']  # too lengthy
            f.write(dumps(obj=data_dict, indent=4) + '\n\n')

        if data_dict.get('error', '') == 'requested block height is bigger then the chain length':  # {"error": "requested block height is bigger then the chain length"}
            print('\nAll blocks scraped!')
            break

        df = DataFrame(data=data_dict)
        print(df)

        df.to_csv(path_or_buf=csv)  # saving data to csv file

        # input('\nPRESS ENTER TO CONTINUE: ')  # debugging

    else:
        START += 1

    height += 1


print('\nSUCCESS')
