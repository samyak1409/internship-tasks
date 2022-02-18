"""
Gridcoin: Retrieve the block level information for all the blocks using the API
(https://node.gridcoin.network/API?q=blockbyheight&height=1) and then use the transaction hash to get the transaction
level using this API (information https://node.gridcoin.network/API?q=tx&hash=[TX HASH])
"""


# Requests: ~2.5M * 2
# API Doc: https://gridcoin.network/api.html
# Currently there is no limit on the amount of queries you can perform.


# IMPORTS:

from requests import get as get_request, RequestException
from json import loads
from concurrent.futures import ThreadPoolExecutor
from csv import writer
from os.path import exists
from os import startfile


# CONSTANTS:

DEBUG = False  # default: False
# Enter custom start, end, and no. of threads if required:
START_HEIGHT = 1  # default: 1
END_HEIGHT = float('inf')  # default: float('inf') (which means scrape all blocks)
THREADS = 1 if DEBUG else 100  # number of concurrent threads to run at once
X = '->'  # child symbol
BLOCK_COLUMNS = ('height',
                 'entropybit',
                 'IsContract',
                 'tx',
                 'netstakeweight',
                 'modifier',
                 'flags',
                 'IsSuperBlock',
                 'querytime',
                 'fees_collected',
                 'mint',
                 'MoneySupply',
                 f'claim{X}mining_id',  # claim->mining_id
                 'difficulty',
                 'size',
                 'location',
                 'time',
                 'username')
TXN_COLUMNS = ('locktime',
               'netstakeweight',
               'txid',
               'contracts',
               f'vout{X}0{X}value',  # vout->0->value
               f'vout{X}0{X}scriptPubKey{X}addresses',  # vout->0->scriptPubKey->addresses
               f'vout{X}0{X}scriptPubKey{X}type',  # vout->0->scriptPubKey->type
               'time')
CSV_FILE = 'Scraped Data.csv'


# FUNCTIONS:

def get_data_from(url: str) -> dict:

    while True:  # sometimes https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_server_errors, which will be fixed after some tries!
        try:
            response = get_request(url=url, stream=False, timeout=1)  # stream and timeout parameters -> VERY IMPORTANT
        except RequestException as e:
            print(f'{type(e).__name__}: {e.__doc__} TRYING AGAIN...')
            continue
        break
    # print(response.status_code)  # debugging

    data = loads(s=response.text)
    # print('Len:', len(data))  # debugging

    if DEBUG:
        print(url)
        # from json import dumps; print(dumps(obj=data, indent=4))  # debugging

    return data


def store_vals_from(data: dict, columns: tuple, index: int) -> None:

    vals = []

    for column in columns:

        if X not in column:  # normal column
            val = data.get(column, '')

        else:  # nested column
            val = data  # copy
            for attr in column.split(X):  # 'claim->mining_id' -> ['claim', 'mining_id']
                try:  # converting index str to index int
                    attr = int(attr)
                except ValueError:  # attr is string only
                    pass
                try:
                    val = val[attr]  # going in
                except KeyError:  # particular attr missing from data_dict
                    val = ''
                    break

        if DEBUG:
            print(f'{column}: {val}')

        vals.append(val)

    scraped_data[index].append(vals)  # scraped_data[index] = [block_data, txn1_data, txn2_data...]


def main(height: int) -> None:

    print(f'\n{height})')

    index = (height - START_HEIGHT) % THREADS  # index of this height's block's data to be inserted in the scraped_data
    # print(index)  # debugging

    block_data = get_data_from(url=f'https://node.gridcoin.network/API?q=blockbyheight&height={height}')
    store_vals_from(data=block_data, columns=BLOCK_COLUMNS, index=index)

    for txn_hash in block_data.get('tx', []):  # list of txn hashes
        store_vals_from(data=get_data_from(url=f'https://node.gridcoin.network/API?q=tx&hash={txn_hash}'), columns=TXN_COLUMNS, index=index)


# MAIN:

print('\nGETTING LATEST BLOCK NUMBER...')
max_height = get_data_from(url='https://node.gridcoin.network/API')['height']
print(max_height)

# Writing column names in CSV:
if not exists(CSV_FILE):
    with open(file=CSV_FILE, mode='w') as f:
        writer(f).writerow(BLOCK_COLUMNS + ('',) + TXN_COLUMNS)
    # startfile(CSV_FILE); exit()  # debugging

# Threading:
for page_num in range(START_HEIGHT, min(END_HEIGHT, max_height)+1, THREADS):  # start, stop, step

    scraped_data = [[] for _ in range(THREADS)]  # [] = x; x[0] = block_data; x[1:] = list_of_txn_data (coz 1 block can have multiple txn)

    # Executing {THREADS} no. of threads at once:
    with ThreadPoolExecutor() as Exec:  # https://youtu.be/IEEhzQoKtQU
        Exec.map(main, range(page_num, page_num+THREADS))

    # Writing the scraped data from {THREADS} no. of threads to the CSV at once:
    with open(file=CSV_FILE, mode='a', newline='') as f:
        w = writer(f)
        for data_ in scraped_data:
            w.writerow(data_[0] + [''] + data_[1])  # block_data, _space_, txn_data
            for txn_data in data_[2:]:  # if multiple txn_data
                w.writerow(['' for _ in range(len(BLOCK_COLUMNS))] + [''] + txn_data)  # empty_block_data, _space_, txn_data
            w.writerow([])  # line gap after a block data

    if DEBUG:
        print('\nFINAL DATA:', scraped_data)
        break


startfile(CSV_FILE)  # automatically open CSV when process completes
print('\nSUCCESS!')
