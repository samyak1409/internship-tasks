"""
Write a Python script to scrape from https://atomscan.com/blocks/1 till https://atomscan.com/blocks/9272083.
We need to scrape every piece of information there.
"""


# IMPORTS:

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.common.exceptions import WebDriverException
from os.path import exists
from openpyxl import Workbook, load_workbook
from datetime import datetime
from os import startfile


# ATTRIBUTES:

website = 'https://atomscan.com'
excel_file = 'Scraped Data.xlsx'
column_names = ['#', 'URL', 'Time', 'Height', 'Number of Transactions', 'Block Hash', 'Proposer']


# CONNECTING TO EXCEL SHEET:

sheet_title = str(datetime.now()).replace(':', ';')  # ':' not allowed as an Excel sheet name

if not exists(excel_file):
    wb = Workbook()
    sheet = wb.active
    sheet.title = sheet_title
else:
    wb = load_workbook(excel_file)
    sheet = wb.create_sheet(title=sheet_title)
    wb.active = sheet

for column_num, column_name in enumerate(iterable=column_names, start=1):
    sheet.cell(row=1, column=column_num, value=column_name)  # inserting column names

wb.save(excel_file)

# print(sheet); exit()  # debugging


# MAIN:

# Website is Dynamic 🤦‍ https://www.geeksforgeeks.org/scrape-content-from-dynamic-websites; https://chromedriver.chromium.org/getting-started

try:
    driver = Chrome()  # webdriver init
except WebDriverException:
    raise SystemExit('''\nERROR: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/getting-started#h.p_ID_36 \n
TL;DR:
1) Download the ChromeDriver binary for your platform from https://chromedriver.chromium.org/downloads
2) Include the ChromeDriver location in your PATH environment variable''')

driver.minimize_window()

print('\nMAKE SURE YOU HAVE A FAST INTERNET CONNECTION AND LAG-FREE SYSTEM!')

try:
    blocks = int(input('\nHow many?: '))
except ValueError:
    print('<empty or non-numeric input>')
else:
    driver.maximize_window()

    for height in range(1, blocks+1):

        row_num = height + 2

        print(f'\nBlock #{height}')
        sheet.cell(row=row_num, column=1, value=height)

        url = f'{website}/blocks/{height}'
        print('URL:', url)
        sheet.cell(row=row_num, column=2, value=url)

        driver.get(url=url)  # open the webpage

        page_html_parsed = BeautifulSoup(markup=driver.page_source, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
        # print(page_html_parsed.prettify()); break  # debugging

        block_details_div = page_html_parsed.find(name='div', class_='card-content block-details').div
        # print(block_details_div.prettify()); break  # debugging

        # 'Time', 'Height', 'Number of Transactions', 'Block Hash', 'Proposer':
        row_div_list = block_details_div.find_all(name='div', class_='columns', recursive=False)
        for column_num, row_div in enumerate(iterable=row_div_list, start=2):
            # print(row_div.prettify()); continue  # debugging
            key_div = row_div.div
            value_div = key_div.next_sibling
            value = value_div.text
            if key_div.text == 'Proposer':
                value = {value: website+value_div.a['href']}
            print(f'{column_names[column_num]}: {value}')
            sheet.cell(row=row_num, column=column_num+1, value=str(value))

        wb.save(excel_file)  # (after every row insertion)

    startfile(excel_file)  # automatically open Excel Sheet when process completes
    print('\nSUCCESS')

finally:
    driver.quit()