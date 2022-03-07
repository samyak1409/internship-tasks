# IMPORTS:

from requests import Session
from json import loads, dumps
from concurrent.futures import ThreadPoolExecutor


# CONSTANTS:

BASE_URL = 'https://explorer-api.mainnet-beta.solana.com'
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


# MAIN:

def main(block: int) -> None:

    payload = {
        "method": "getConfirmedBlock",
        "jsonrpc": "2.0",
        "params": [block, {"commitment": "confirmed"}],
        "id": ""
    }

    data = loads(s=session.post(url=BASE_URL, json=payload).text)['result']

    print(f"\n{block}) Items: {len(data)}")

    if DEBUG:
        print(dumps(obj=data, indent=4))
        print('Transactions:', len(data['transactions']))


# SESSION INIT:

with Session() as session:

    session.headers = HEADERS
    session.stream = False  # stream off for all the requests of this session

    # THREADING:
    for page_num in range(1, 1_000, THREADS):  # start, stop, step
        with ThreadPoolExecutor() as Exec:
            Exec.map(main, range(page_num, page_num+THREADS))
        if DEBUG:
            break


print('\nSUCCESS!')
