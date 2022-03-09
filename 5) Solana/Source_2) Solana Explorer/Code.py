"""
Using https://github.com/samyak1409/internship-tasks#9-always-check-for-the-hidden-api-when-web-scraping-inspect---network---xhr---name---some-get-request---response

Total Blocks: ~120M
"""


# IMPORTS:

from requests import Session, RequestException
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from csv import writer, Error
from os import stat, chdir
from glob import iglob
from time import perf_counter


start_time = perf_counter()


# CONSTANTS:

URL = 'https://explorer-api.mainnet-beta.solana.com'
DEBUG = False  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
HEADERS = {
    "authority": "explorer-api.mainnet-beta.solana.com",
    "sec-ch-ua": '"(Not(A:Brand";v="8", "Chromium";v="98", "Google Chrome";v="98"',
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "content-type": "application/json",
    "accept": "*/*",
    "origin": "https://explorer.solana.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://explorer.solana.com",
    "accept-language": "en-US,en;q=0.9"
}
COLUMNS = ('blockHeight', 'blockTime', 'blockhash', 'parentSlot', 'previousBlockhash', 'rewards', 'transactions')
DATA_DIR = 'Scraped Data'
MAX_SIZE = 32  # of CSV you want to be (in MB)


# MAIN FUNCTION:

def main(block: int) -> None:

    # Getting Request's Response:
    payload = {
        "method": "getConfirmedBlock",
        "jsonrpc": "2.0",
        "params": [block, {"commitment": "confirmed"}],
        "id": ""
    }
    while True:
        try:
            response = session.post(url=URL, json=payload)
        except RequestException as e:
            if DEBUG:
                print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
        else:
            if response.status_code == 200:
                break
            else:  # bad response
                if DEBUG:
                    print(f'{response.status_code}: {response.reason} TRYING AGAIN...')

    data = response.json()['result']
    print('\n' + f"{block}) Data Items: {len(data)}; Transactions: {len(data['transactions'])}")

    data['blockHeight'] = block  # block height was empty for some reason

    if DEBUG:
        print(dumps(obj=data, indent=4))

    data_dict[block] = data.values()


# SESSION INIT:

with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    chdir(DATA_DIR)

    print('\nGetting start and last block number...')
    try:
        start = max(map(lambda name: int(name.split('.csv')[0]), iglob(pathname='*.csv')))
    except ValueError:
        start = 1
    max_block = session.post(url=URL, json={"method": "getEpochInfo", "jsonrpc": "2.0", "params": [], "id": ""}).json()['result']['absoluteSlot']
    print(start, max_block)

    csv = None

    # THREADING:
    for block_num in range(start, max_block+1, THREADS):  # start, stop, step

        if not csv or stat(csv).st_size >= 1_048_576 * MAX_SIZE:  # at most {MAX_SIZE} MB of data in one CSV
            csv = f'{block_num}.csv'  # new CSV
            # Writing column names in CSV:
            with open(file=csv, mode='w', newline='') as f:
                writer(f).writerow(COLUMNS)
            # startfile(CSV); exit()  # debugging

        while True:  # writing to CSV give error sometimes, should be fixed on retry
            # Using dict so that the data is kept sorted:
            data_dict = {num: None for num in range(block_num, block_num+THREADS)}  # {block_number: block_transactions_data}

            # Executing {THREADS} no. of threads at once:
            with ThreadPoolExecutor() as Exec:
                Exec.map(main, range(block_num, block_num+THREADS))

            # Writing the data scraped from {THREADS} no. of threads to the CSV:
            with open(file=csv, mode='a', newline='') as f:
                try:
                    writer(f).writerows(data_dict.values())
                except Error:  # "_csv.Error: iterable expected, not NoneType" for some reason
                    continue  # try again
                break

        if DEBUG:
            break


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')
