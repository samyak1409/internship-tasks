"""
Bytecoin: Here, you will need to get the data from the webpage. Make sure to get all the information including the
number of transactions (https://explorer.bytecoin.org/block?height=2033923)
"""


# IMPORTS:

from requests import Session, RequestException
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook
from os import stat, chdir, startfile
from glob import iglob
from time import perf_counter, sleep


start_time = perf_counter()


# CONSTANTS:

BASE_URL = 'https://explorer.bytecoin.org'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
COLUMNS = ('Height', 'Timestamp', 'Transactions')
DEBUG = True  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
DATA_DIR = 'Scraped Data'  # path to data dir
MAX_SIZE = 32  # of Excel, you want to be (in MB)


# MAIN FUNCTION:

def main(block_height: int) -> None:

    # Getting Request's Response:
    while True:
        try:
            response = session.get(url=f'{BASE_URL}/block?height={block_height}')
        except RequestException as e:
            print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:
            if response.status_code == 200:
                break
            else:  # bad response
                print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                sleep(1)  # take a breath

    soup = BeautifulSoup(markup=response.text, features='html.parser')
    # print(soup.prettify())  # debugging

    timestamp_data = soup.find(name='span', id='block_timestamp').parent
    # print(timestamp_data.prettify())  # debugging
    timestamp_str = list(timestamp_data.stripped_strings)[1]

    txn_heading = soup.find_all(name='p', class_='bigbold')[1]
    # print(txn_heading.prettify())  # debugging
    txn_count = int(txn_heading.text.split('-')[1].strip())

    print('\n' + f'{block_height}) Timestamp: {timestamp_str}; Transactions: {txn_count}')

    data_dict[block_height] = (block_height, timestamp_str, txn_count)


# SESSION INIT:

with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    chdir(DATA_DIR)

    print('\nGetting start and stop block number...')
    try:
        start = max(map(lambda name: int(name.split('.xlsx')[0]), iglob('*.xlsx')))
    except ValueError:  # no files were there in the dir
        start = 1
    stop = int(next(filter(lambda num: num.isnumeric(), list(BeautifulSoup(session.get(f'{BASE_URL}/block?height=0').text, 'html.parser').a.parent.stripped_strings)[1].split())))
    print(start, stop)

    # THREADING:

    excel = None

    for height in range(start, stop, THREADS):  # start, stop, step

        if not excel or stat(excel).st_size >= 1_048_576 * MAX_SIZE:  # at most {MAX_SIZE} MB of data in one Excel
            excel = f'{height}.xlsx'  # new Excel
            wb = Workbook()
            sheet = wb.active
            sheet.append(COLUMNS)  # writing column names in Excel; https://openpyxl.readthedocs.io/en/stable/#:~:text=Sample%20code
            wb.save(excel)
            # startfile(excel); print(sheet); exit()  # debugging

        # Using dict so that the data is kept sorted:
        data_dict = {num: None for num in range(height, height+THREADS)}  # {block_height: block_data}

        # Executing {THREADS} no. of threads at once:
        with ThreadPoolExecutor() as Exec:
            Exec.map(main, range(height, height+THREADS))

        # Writing the data scraped from {THREADS} no. of threads to the Excel:
        for row in filter(None, data_dict.values()):  # filter -> consider only non-empty values
            sheet.append(row)
        wb.save(excel)

        if DEBUG:
            startfile(excel)
            break


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')


# TODO: resume functionality
