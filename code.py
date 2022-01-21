from requests import get as get_request
from bs4 import BeautifulSoup
from itertools import count


website = 'https://coinmarketcap.com'


for page_num in count(start=1):  # infinite loop

    webpage = f'{website}/?page={page_num}'
    response = get_request(url=webpage)
    print('\n', webpage, response, '\n')

    if response.status_code == 200:  # everything's okay

        web_html = response.text
        # print(web_html); input()  # debugging

        soup = BeautifulSoup(markup=web_html, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
        # print(soup.prettify()); input()  # debugging

        tags = soup.find(name='tbody').find_all(class_=['sc-16r8icm-0 escjiH', 'sc-1rqmhtg-0 jUUSMS'])
        for num, tag in enumerate(tags, start=1):

            num += (page_num-1) * 100
            # print(tag.prettify(), '\n'); continue  # debugging

            currency = tag.a['href']
            # print(f'{num}) {currency}'); continue  # debugging

            currency_web = website + currency
            print(f'{num}) {currency_web}')

            # MAIN:

    elif response.status_code == 404:  # webpage not found
        print('Stopping... \n')
        break  # stop looping

    else:
        from time import sleep
        sleep(1)
        exit(response.reason)


print('SUCCESS')
