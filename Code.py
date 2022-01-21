from requests import get as get_request
from bs4 import BeautifulSoup
from itertools import count
from json import loads


source_website = 'https://coinmarketcap.com'


for page_num in count(start=1):  # infinite loop

    webpage = f'{source_website}/?page={page_num}'
    response = get_request(url=webpage)
    print('\n', webpage, response, '\n')

    if response.status_code == 200:  # everything's okay

        soup = BeautifulSoup(markup=response.text, features='html.parser')  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers
        # print(soup.prettify()); input()  # debugging

        tags = soup.find(name='tbody').find_all(class_=['sc-16r8icm-0 escjiH', 'sc-1rqmhtg-0 jUUSMS'])
        for num, tag in enumerate(tags, start=1):

            num += (page_num-1) * 100

            # print(tag.prettify(), '\n'); continue  # debugging

            currency = tag.a['href']
            # print(f'{num}) {currency}'); continue  # debugging

            currency_web = source_website + currency
            print(f'{num}) {currency_web} \n')

            # MAIN:
            soup = BeautifulSoup(markup=get_request(url=currency_web).text, features='html.parser')
            # print(soup.prettify()); input()  # debugging

            json_str = soup.find(name='script', id='__NEXT_DATA__').text  # found with the help of "View page source"
            # print(json_str); input()  # debugging

            json_dict = loads(s=json_str)  # parse
            # from json import dumps; print(dumps(obj=json_dict, indent=8)); input()  # debugging

            urls_dict = json_dict['props']['initialProps']['pageProps']['info']['urls']
            # print(urls_dict); input()  # debugging

            for attr, url in urls_dict.items():
                print(f'{attr}: {url}')
            print()  # spacing

    elif response.status_code == 404:  # webpage not found
        print('Stopping... \n')
        break  # stop looping

    else:
        from time import sleep
        sleep(1)
        exit(response.reason)


print('SUCCESS')
