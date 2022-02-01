"""
Write a Python script to scrape from https://atomscan.com/blocks/1 till the latest block.
We need to scrape every piece of information there.
"""


# IMPORTS:

from itertools import count
from requests import get as get_request
from bs4 import BeautifulSoup


# MAIN:

for height in count(start=1):  # infinite loop

    print(f'\nBlock #{height}')

    response = get_request(url=f'https://atomscan.com/blocks/{height}')

    if response.status_code == 200:  # everything's okay

        page_html_parsed = BeautifulSoup(markup=response.text, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
        print(page_html_parsed.prettify()); exit()  # debugging

    else:  # something went wrong

        for key, value in response.__dict__.items():
            print(f'{key}: {value}')  # debugging

        exit()


print('\nSUCCESS')
