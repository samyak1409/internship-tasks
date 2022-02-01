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
from itertools import count
from pandas import DataFrame
from os.path import exists


# MAIN:

for height in count(start=5200791):  # infinite loop

    csv = f'Scraped Data\\{height}.csv'

    if not exists(path=csv):  # if not already scraped

        print(f'\n#{height}')

        response = get_request(url=f'https://api.cosmos.network/blocks/{height}')

        if response.status_code == 200:  # everything's good

            data_dict = loads(s=response.text)
            print(dumps(obj=data_dict, indent=4))

            df = DataFrame(data=data_dict)
            # print(df)  # debugging

            df.to_csv(path_or_buf=csv)  # saving data to csv file

            # input('\nPRESS ENTER TO CONTINUE: ')  # debugging

        else:  # something went wrong

            for key, value in response.__dict__.items():
                print(f'{key}: {value}')  # debugging

            exit()


print('\nSUCCESS')
