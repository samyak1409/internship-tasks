# Internship Tasks

This repository contains the codes of Web Scraping tasks of my Internship.


## Installing the Dependencies

After downloading this project to your PC, open the project folder, there, open your [command-line interpreter](https://en.wikipedia.org/wiki/List_of_command-line_interpreters#:~:text=In%20computing%2C%20a%20command-line%20interpreter%2C%20or%20command%20language%20interpreter%2C%20is%20a%20blanket%20term%20for%20a%20certain%20class%20of%20programs%20designed%20to%20read%20lines%20of%20text%20entered%20by%20a%20user%2C%20thus%20implementing%20a%20command-line%20interface.) (e.g. Command Prompt for Windows), and run the following:
```
pip install -r requirements.txt
```


## Coding Standards

- Properly formatted codes ([PEP 8](https://www.python.org/dev/peps/pep-0008) ✅)
- Proper comments and descriptive variable names 🙌



## Some Helper Notes & Resources:


#### 1) [Official `Requests` Doc](https://docs.python-requests.org)


#### 2) Want to Try Something / Play with Requests & Responses?

- [httpbin.org](https://httpbin.org)
- [Example Domain](https://www.example.com)


#### 3) Sending Multiple Requests to Same Host?

#### Use [Session](https://docs.python-requests.org/en/latest/user/advanced/#session-objects)

- [Advantages](https://en.wikipedia.org/wiki/HTTP_persistent_connection#Advantages)

```py
from requests import Session

with Session() as session:  # requests session init

    session.stream = False  # stream off for all the requests of this session

    response = session.get(url='https://www.example.com')
    print(response.status_code)
```


#### 4) Complete HTML is not Loading using `Requests` because it's a Dynamic Website?

#### Use [Selenium](https://pypi.org/project/selenium)

- [Scrape content from dynamic websites](https://www.geeksforgeeks.org/scrape-content-from-dynamic-websites)

```py
from selenium.webdriver import Chrome
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from time import sleep

def get_parsed_page_html():
    return BeautifulSoup(markup=driver.page_source, features='html.parser')

def wait_to_load():
    print('SLOW INTERNET: PLEASE WAIT...')
    sleep(1)

try:
    driver = Chrome()  # webdriver init
except WebDriverException:
    raise SystemExit('''\nERROR: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/getting-started#h.p_ID_36 \n
TL;DR:
1) Download the ChromeDriver binary for your platform from https://chromedriver.chromium.org/downloads
2) Include the ChromeDriver location in your PATH environment variable''')

driver.maximize_window()  # window must not be minimized, else page will load in greater time

driver.get(url='https://www.example.com')  # open the webpage

# wait_to_load()  # in case still loading

html = get_parsed_page_html()
# print(html.prettify())  # debugging

print(html.p.text)

driver.quit()
```


#### 5) HUGE Number of Requests to Send?

#### Use [Threading](https://docs.python.org/3/library/threading.html)

- [Python Threading Tutorial: Run Code Concurrently Using the Threading Module](https://youtu.be/IEEhzQoKtQU)

```py
from concurrent.futures import ThreadPoolExecutor

THREADS = 10

def main(i: int) -> None:
    print(i)

# Executing {THREADS} no. of threads at once:
with ThreadPoolExecutor() as Exec:
    Exec.map(main, range(1, THREADS+1))
```


#### 6) Website have Rate Limit?

#### Use [Proxies](https://en.wikipedia.org/wiki/Proxy_server)

- [Creating a Reliable, Random Web Proxy Request Application using Python](https://youtu.be/n3uSyqoBgQI)

```py
from requests import get as get_request, RequestException
from bs4 import BeautifulSoup
from random import choice

# Using free proxies here, which is very slow, use paid proxies if possible.
html = BeautifulSoup(markup=get_request(url='https://www.sslproxies.org').text, features='html.parser')

proxies_raw = html.find(name='textarea').text.strip()
# print(proxies_raw)  # debugging

proxies = proxies_raw.split('\n')[3:]
# print(proxies, len(proxies))  # debugging

while True:
    proxy = choice(proxies)
    print(proxy)
    try:
        print(get_request('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, stream=False, timeout=5).json())
        break
    except RequestException:
        pass
```


#### 7) [Official `Beautiful Soup` Doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc)



## Ciao!👋
