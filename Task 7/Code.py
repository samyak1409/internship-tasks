"""
Filecoin: Use this API (https://filfox.info/api/v1/message/list?pageSize=100&page=1) and keep incrementing the page
variable to get all the data from the json file
"""


# Requests: ~7M
# API Doc: https://filfox.info/api/v1/?
# LIMIT?


# IMPORTS:

from requests import get as get_request, RequestException
from json import loads
from concurrent.futures import ThreadPoolExecutor


# CONSTANTS:

BASE_URL = 'https://filfox.info/api/v1/message/list'
DEBUG = True  # default: False
# Enter custom start, end, and no. of threads if required:
START_PAGE = 1  # default: 1
END_PAGE = float('inf')  # default: float('inf') (which means scrape all blocks)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
BLOCK_COLUMNS = ('page', 'cid', 'height', 'timestamp', 'from', 'to', 'value', 'method', 'receipt')
CSV_FILE = 'Scraped Data.csv'


# FUNCTIONS:

def get_data_from(url: str) -> dict:

    if DEBUG:
        print(url)

    while True:  # sometimes https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_server_errors, which will be fixed after some tries!
        try:
            response = get_request(url=url, stream=False, timeout=1)  # stream and timeout parameters -> VERY IMPORTANT
        except RequestException as e:
            print(f'{type(e).__name__}: {e.__doc__} TRYING AGAIN...')
            continue
        break
    # print(response.status_code)  # debugging

    data = loads(s=response.text)
    # print('LEN:', len(data))  # debugging
    # from json import dumps; print(dumps(obj=data, indent=4))  # debugging

    return data


def main(page: int) -> None:

    print(f'\n{page})')

    messages = get_data_from(url=f'{BASE_URL}?pageSize=100&page={page}')['messages']
    print('LEN:', len(messages))  # debugging
    from json import dumps; print(dumps(obj=messages, indent=4))  # debugging


# MAIN:

print('\nGETTING LATEST BLOCK NUMBER...')
total_count = get_data_from(url=BASE_URL)['totalCount']
print(total_count)

# Threading:
for page_num in range(START_PAGE, int(min(END_PAGE, total_count))+1, THREADS):  # start, stop, step

    # Executing {THREADS} no. of threads at once:
    with ThreadPoolExecutor() as Exec:  # https://youtu.be/IEEhzQoKtQU
        Exec.map(main, range(page_num, page_num+THREADS))

    if DEBUG:
        break


print('\nSUCCESS!')
