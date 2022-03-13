"""
Source: BG API from https://explorer.solana.com/block/125000000

Using https://github.com/samyak1409/internship-tasks#9-always-check-for-the-hidden-api-when-web-scraping-inspect---network---xhr---name---some-get-request---response

Total Blocks: ~125M
"""


# IMPORTS:

from requests import Session, RequestException
from json import dumps, JSONDecodeError
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook
from os import stat, chdir, startfile
from glob import iglob
from time import perf_counter, sleep, strftime, gmtime


start_time = perf_counter()


# CONSTANTS:

URL = 'https://explorer-api.mainnet-beta.solana.com'
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
COLUMNS = ('blockHeight', 'blockTime', 'blockhash', 'txn_count', 'transactions ->')
DEBUG = False  # (default: False)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
DATA_DIR = 'Scraped Data'  # path to data dir
MAX_SIZE = 32  # of Excel, you want to be (in MB)


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
            print(f'{type(e).__name__}:', e.__doc__.split('\n')[0], 'TRYING AGAIN...')
            sleep(1)  # take a breath
        else:
            if response.status_code == 200:
                try:
                    data = response.json()
                except JSONDecodeError as e:  # sometimes json is not being loaded completely (IDK why)
                    print(e, 'TRYING AGAIN...')
                    sleep(1)  # take a breath
                else:
                    break
            else:  # bad response
                print(f'{response.status_code}: {response.reason} TRYING AGAIN...')
                sleep(1)  # take a breath

    error = data.get('error')  # "error": {"code": -32009, "message": "Slot 86804 was skipped, or missing in long-term storage"}
    if error:
        print('\n' + f'{block}) ERROR: {error}')
        del data_dict[block]  # deleting placeholder of the block
        return

    data = data['result']  # data we want

    txns = data.pop('transactions')
    txn_count = len(txns)

    print('\n' + f'{block}) Data Items: {len(data)+1}; Transactions: {txn_count}')  # (+1 -> for popped 'transactions')

    data['blockHeight'] = block  # block height is empty for some reason

    block_time = data['blockTime']
    if block_time is not None:  # https://stackoverflow.com/questions/12400256/converting-epoch-time-into-the-datetime
        data['blockTime'] = strftime('%Y-%m-%d %H:%M:%S', gmtime(block_time))

    del data['parentSlot'], data['previousBlockhash'], data['rewards']

    data['txn_count'] = txn_count  # adding

    # Strategy 1:
    """
    acc_keys_list = data['transactions'] = [txn['transaction']['message']['accountKeys'] for txn in txns]  # altering the txn data to only the desired data
    # Searching accountKeys which are common in all the accountKeys list (which is useless data):
    common_keys = min(acc_keys_list, key=len, default=[])  # getting the shortest accountKeys list (for efficient search)
    for acc_keys in acc_keys_list:
        for common_key in common_keys:
            if common_key not in acc_keys:  # logic: if a key is not there in ith key_list => key is not common
                common_keys.remove(common_key)
    print(common_keys)  # debugging
    # Removing:
    for i in range(txn_count):
        for common_key in common_keys:
            data['transactions'][i].remove(common_key)
        if not data['transactions'][i]:  # list emptied
            del data['transactions'][i]
    """
    # Strategy 2:
    # Altering the txn data to save only the desired data + Removing duplicate keys:
    keys_set = set()  # for saving the unique keys
    acc_keys_list = []
    for txn in txns:
        acc_keys = []
        for key in txn['transaction']['message']['accountKeys']:
            if key not in keys_set:
                acc_keys.append(key)  # storing the key
                keys_set.add(key)  # adding the key to tracking
        if acc_keys:  # only if acc_keys != []
            acc_keys_list.append(acc_keys)
    data['transactions'] = acc_keys_list

    if DEBUG:
        print(dumps(obj=data, indent=4))

    data_dict[block] = list(data.values())


# SESSION INIT:

with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    chdir(DATA_DIR)

    print('\nGetting start block number...')
    try:
        start = min(map(lambda name: int(name.split('.xlsx')[0]), iglob(pathname='*.xlsx')))
    except ValueError:  # no files were there in the dir
        start = session.post(url=URL, json={"method": "getEpochInfo", "jsonrpc": "2.0", "params": [], "id": ""}).json()['result']['absoluteSlot']  # max block
        start -= start % 100  # 124514773 -> 124514700
    print(start)

    # THREADING:

    excel = None

    for block_num in range(start, 0, -THREADS):  # start, stop, step

        if not excel or stat(excel).st_size >= 1_048_576 * MAX_SIZE:  # at most {MAX_SIZE} MB of data in one Excel
            excel = f'{block_num}.xlsx'  # new Excel
            wb = Workbook()
            sheet = wb.active
            sheet.append(COLUMNS)  # writing column names in Excel; https://openpyxl.readthedocs.io/en/stable/#:~:text=Sample%20code
            wb.save(excel)
            # startfile(excel); print(sheet); exit()  # debugging

        # Using dict so that the data is kept sorted:
        data_dict = {num: None for num in range(block_num, block_num-THREADS, -1)}  # {block_number: block_transactions_data}

        # Executing {THREADS} no. of threads at once:
        with ThreadPoolExecutor() as Exec:
            Exec.map(main, range(block_num, block_num-THREADS, -1))

        # Writing the data scraped from {THREADS} no. of threads to the Excel:
        for row in filter(None, data_dict.values()):  # filter -> consider only non-empty values
            sheet.append(row[:-1] + list(map(str, row[-1])))  # row[-1] = list of list, so,
            # 1) mapping the inner lists to str so that it can be inserted in the Excel, 2) again converting it to a list in order to add with other list
        wb.save(excel)

        if DEBUG:
            startfile(excel)
            break


print('\n' + f'Successfully finished in {int(perf_counter()-start_time)}s.')


# Possible To Do:
# Resume (from the last scraped block) Functionality
