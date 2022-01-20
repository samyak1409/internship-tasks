from requests import get as get_request
from bs4 import BeautifulSoup


website = 'https://coinmarketcap.com'

web_response = get_request(url=website)
# print(web_response); input()  # debugging

if web_response.status_code == 200:  # everything's okay

    web_html = web_response.text
    # print(web_html); input()  # debugging

    soup = BeautifulSoup(markup=web_html, features='html.parser')
    # print(soup.prettify()); input()  # debugging

    tags = soup.find(name='tbody').find_all(name='div', class_='sc-16r8icm-0 escjiH')
    for tag in tags:
        # print(tag.prettify(), '\n'); continue  # debugging

        currency = tag.a.get('href')
        # print(currency); continue  # debugging

        currency_web = website + currency
        print(currency_web); continue  # debugging

        # MAIN:


else:
    print(web_response)
