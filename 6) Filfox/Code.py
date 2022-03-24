"""
Filecoin: Use this API (https://filfox.info/api/v1/message/list?pageSize=100&page=1) and keep incrementing the page
variable to get all the data from the json file
"""


# IMPORTS:

from requests import Session, RequestException
from json import loads
from concurrent.futures import ThreadPoolExecutor
from csv import writer, DictWriter
from os.path import exists
from os import startfile
from time import sleep


# CONSTANTS:

BASE_URL = 'https://filfox.info/api/v1/message/list'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
DEBUG = False  # default: False
# Enter custom start, end, and no. of threads if required:
START_PAGE = 1  # default: 1
END_PAGE = 100  # default: float('inf') (which means scrape all blocks)
THREADS = 1 if DEBUG else 10  # number of concurrent threads to run at once
BLOCK_COLUMNS = ('page', 'cid', 'height', 'timestamp', 'from', 'to', 'value', 'method', 'receipt')
CSV_FILE = 'Scraped Data.csv'


# FUNCTIONS:

def get_data_from(url: str) -> dict:

    if DEBUG:
        print(url)

    while True:  # sometimes https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_server_errors, which will be fixed after some tries!
        try:
            response = session.get(url=url)
        except RequestException as e:
            print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:
            if response.status_code == 200:
                break
            else:
                print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                sleep(1)  # take a breath

    data = loads(s=response.text)
    # print('LEN:', len(data))  # debugging
    # from json import dumps; print(dumps(obj=data, indent=4))  # debugging

    return data


def main(page: int) -> None:

    print(f'\n{page})')

    messages = get_data_from(url=f'{BASE_URL}?pageSize=100&page={page}')['messages']
    # print('LEN:', len(messages))  # debugging
    # from json import dumps; print(dumps(obj=messages, indent=4))  # debugging

    scraped_data[page] = messages


# MAIN:

# Writing column names in CSV:
if not exists(CSV_FILE):
    with open(file=CSV_FILE, mode='w') as f:
        writer(f).writerow(BLOCK_COLUMNS)
    # startfile(CSV_FILE); exit()  # debugging

# SESSION INIT:
with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    print('\nGETTING LATEST BLOCK NUMBER...')
    total_count = get_data_from(url=BASE_URL)['totalCount'] // 100
    print(total_count)

    # Threading:
    for page_num in range(START_PAGE, int(min(END_PAGE, total_count))+1, THREADS):  # start, stop, step

        scraped_data = {page: None for page in range(page_num, page_num+THREADS)}  # {page_number: message_dict_list}

        # Executing {THREADS} no. of threads at once:
        with ThreadPoolExecutor() as Exec:  # https://youtu.be/IEEhzQoKtQU
            Exec.map(main, range(page_num, page_num+THREADS))

        # Writing the data scraped from {THREADS} no. of threads to the CSV:
        with open(file=CSV_FILE, mode='a', newline='') as f:
            for page, message_dict_list in scraped_data.items():
                DictWriter(f=f, fieldnames=BLOCK_COLUMNS, restval=page).writerows(rowdicts=message_dict_list)  # https://docs.python.org/3/library/csv.html#csv.DictWriter
                writer(f).writerow([])  # line gap after a block data

        if DEBUG:
            from pprint import pprint
            pprint(scraped_data)
            break


startfile(CSV_FILE)  # automatically open CSV when process completes
print('\nSUCCESS!')
