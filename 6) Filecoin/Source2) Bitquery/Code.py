# IMPORTS:
from requests import post
from json import dumps
from pandas import DataFrame
from os import startfile


# CONSTANTS:
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-csrf-token": "kYZglHtnsmAOv+f7i+tb10p0WPlrGSiNHnPBw4twjYhDf8lzmsnEPoGzUw+ygko1rbAXcYH1xc2TAV1Ze6hgVQ==",
    "cookie": "_ga=GA1.2.684485808.1648571196; _gid=GA1.2.106464027.1648571196; _gat_gtag_UA_115049964_3=1; _fbp=fb.1.1648571196078.660439960; _explorer_session=n%2Buc1NUavxm%2BNqUknZbXIQrHjFRLcfuVKkrVHPttkF274tOoUmSZZOn9boI64nkrdREXjkZkF6%2F3NNPe9XQPLyJci%2BQW21Oxhsq5gLzXJJOsT%2F%2BS%2BA8zdW1m%2Bcp%2FY2zTbfOYSIjqg8ghNEbxO8isAMOZJ0I%2B9n43XLKeS%2FwbELKWfQZ5ZLoGhkQoBnADskrinVb8B1X2qoLV9r7KMGCnY%2BY7TCvEw05bt%2F1uvd5ViRLhAUd9N3%2FLeV9ZJqsWa1L0ErgoPQtxcR9WLqNXAM8eUokSWVyd2VwXqNY8GIaIxGml1UfhbiJeQKf36wAM6VQHwv%2BAML0JYJ%2BrzlYIIzb1Mys%3D--QhCTLTdmbMb4l6RL--W5F%2Ftsbb2FmBadur8lsBGQ%3D%3D",
    "Referer": "https://explorer.bitquery.io/filecoin?till=2022-01-31",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
DEBUG = False  # (default: False)
MAX_LIMIT = 10 if DEBUG else 25_000
EXCEL = 'Data.xlsx'


# MAIN:

skip = 0
block_list = []

print()  # spacing

while True:

    payload = {"operationName": None, "variables": {"limit": MAX_LIMIT, "offset": skip, "network": "filecoin", "from": None, "till": "2022-01-31T23:59:59", "dateFormat": "%Y-%m"}, "query": "query ($network: FilecoinNetwork!, $limit: Int!, $offset: Int!, $from: ISO8601DateTime, $till: ISO8601DateTime) {\n filecoin(network: $network) {\n blocks(options: {desc: \"height\", limit: $limit, offset: $offset}, date: {since: $from, till: $till}) {\n timestamp {\n time(format: \"%Y-%m-%d %H:%M:%S\")\n }\n height\n count\n messageCount\n reward\n minerTips\n }\n }\n}\n"}
    response = post('https://explorer.bitquery.io/proxy_graphql', headers=HEADERS, json=payload).json()
    print(dumps(response, indent=4))  # debugging

    blocks = response['data']['filecoin']['blocks']
    if not blocks:
        break  # all data scraped
    for block in blocks:
        block['timestamp'] = block['timestamp']['time']  # cleaning timestamp ({"time": "2022-01-31 23:50:30"} -> "2022-01-31 23:50:30")
        block_list.append(block)  # storing the block data to the list

    if DEBUG and skip == MAX_LIMIT:
        break

    skip += MAX_LIMIT

DataFrame(data=block_list).to_excel(EXCEL, index=False)  # writing the stored data to excel
startfile(EXCEL)

print('\n' + 'SUCCESS!')
