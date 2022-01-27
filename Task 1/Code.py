# I need the entire data on page https://www.asicminervalue.com/ --Model, Release, Hashrate, Power, Noise, Algo, Profitability, and the link associated with each model
# Using the link associated with each model -you will need to parse the specific page for each of the hardware - For example, for Jasminer - we need all its data -- profitability, Algorithms (Algorythm Hashrate Consumption Efficiency Profitability), Description, All fields in specifications, minable coins, mining pools, all the information in Where to buy and cloud mining information (including the html links).


# IMPORTS:

from requests import get as get_request
from bs4 import BeautifulSoup


# ATTRIBUTES:

website = 'https://www.asicminervalue.com'


# SCRAPING PART 1:

website_html_parsed = BeautifulSoup(markup=get_request(url=website).text, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
# print(website_html_parsed.prettify()); exit()  # debugging

model_html_list = website_html_parsed.find(name='tbody').find_all(name='tr')  # list of HTML of all the miner models
# print(model_html_list); exit()  # debugging

for num, model_html in enumerate(iterable=model_html_list, start=1):

    # print(model_html.prettify(), '\n'); input()  # debugging

    miner_sub_url = model_html.find(name='a')['href']
    # print(f'{num}) {miner_sub_url}'); continue  # debugging

    miner_page = website + miner_sub_url
    print('\n' + f'{num}) {miner_page} \n')

    # SCRAPING PART 2:
