# I need the entire data on page https://www.asicminervalue.com/ --Model, Release, Hashrate, Power, Noise, Algo, Profitability, and the link associated with each model
# Using the link associated with each model -you will need to parse the specific page for each of the hardware - For example, for Jasminer - we need all its data -- profitability, Algorithms (Algorythm Hashrate Consumption Efficiency Profitability), Description, All fields in specifications, minable coins, mining pools, all the information in Where to buy and cloud mining information (including the html links).


# IMPORTS:

from requests import get as get_request
from bs4 import BeautifulSoup
from unicodedata import normalize
from os.path import exists
from openpyxl import Workbook, load_workbook
from datetime import datetime
from os import startfile


# ATTRIBUTES:

website = 'https://www.asicminervalue.com'
excel_file = 'Scraped Data.xlsx'
column_names = ['#', 'Model', 'Release', 'Hashrate', 'Power', 'Noise', 'Algo', 'Profitability', 'Link']


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


# SCRAPING PART 1:

website_html_parsed = BeautifulSoup(markup=get_request(url=website).text, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
# print(website_html_parsed.prettify()); exit()  # debugging

model_html_list = website_html_parsed.find(name='tbody').find_all(name='tr')  # list of HTML of all the miner models
# print(model_html_list); exit()  # debugging

for sr_num, model_html in enumerate(iterable=model_html_list, start=1):

    row_num = sr_num + 2

    print(f'\n{sr_num}')
    sheet.cell(row=row_num, column=1, value=sr_num)

    # print(model_html.prettify(), '\n')  # debugging

    div_tags = model_html.find_all(name='div')
    # print(div_tags)  # debugging
    values = list(map(lambda div_tag: normalize('NFKD', div_tag.text).strip(), div_tags))[3:][:7]  # https://stackoverflow.com/a/34669482
    # print(values)  # debugging

    # Algos' Name Correction: (if there will be multiple algos of a model, extraction using ".text" will give the number of algos and not their names)
    try:  # checking if the value is a number or not
        int(values[5])
    except ValueError:  # value is not a number => everything's good
        pass
    else:  # value is a number => there were multiple algos of this model
        values[5] = div_tags[8].span['title']  # correcting

    for column_num, value in enumerate(iterable=values, start=2):
        print(value)
        sheet.cell(row=row_num, column=column_num, value=value)

    model_page = website + model_html.find(name='a')['href']
    print(model_page)
    sheet.cell(row=row_num, column=9, value=model_page)

    wb.save(excel_file)  # (after every insertion)

    # SCRAPING PART 2:

    #


startfile(excel_file)  # automatically open Excel Sheet when process completes

print('\nSUCCESS')
