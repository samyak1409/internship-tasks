# Internship Tasks

This repository contains the codes of Web Scraping tasks of my Internship.



## [Certificate](https://internshala.com/student/certificate/92235473/2F7EE0CB-D280-ABE0-E799-47450F9910C0)

<img src="https://internshala.com/uploads/student_certificates/61faf9b3cc7901643837875.png">



## Installing the Dependencies

After downloading this project to your PC, open the project folder, there, open your [command-line interpreter](https://en.wikipedia.org/wiki/List_of_command-line_interpreters#:~:text=In%20computing%2C%20a%20command-line%20interpreter%2C%20or%20command%20language%20interpreter%2C%20is%20a%20blanket%20term%20for%20a%20certain%20class%20of%20programs%20designed%20to%20read%20lines%20of%20text%20entered%20by%20a%20user%2C%20thus%20implementing%20a%20command-line%20interface.) (e.g. Command Prompt for Windows), and run the following:
```
pip install -r requirements.txt
```



## Coding Standards

- Properly formatted codes ([PEP 8](https://www.python.org/dev/peps/pep-0008) ✅)
- Proper comments and descriptive variable names 🙌



## Some Helper Notes & Resources:


#### 0) [Web Scraping Tips for Beginners](https://youtu.be/QEANQsoEmHI)


#### 1) [Official `Requests` Doc](https://docs.python-requests.org/en/latest)


#### 2) Want to Try Something / Play with Requests & Responses?

- [httpbin.org](https://httpbin.org)
- [Example Domain](https://www.example.com)


#### 3) Sending Multiple Requests to Same Host?

**Use [Session](https://docs.python-requests.org/en/latest/user/advanced/#session-objects)**

- [Advantages](https://en.wikipedia.org/wiki/HTTP_persistent_connection#Advantages)
- [Want Faster HTTP Requests? Use A Session with Python!](https://youtu.be/IDhuUpeF1n0)

```py
from requests import Session

with Session() as session:  # requests session init

    session.stream = False  # stream off for all the requests of this session

    response = session.get(url='https://www.example.com')
    print(response.status_code)
```


#### 4) Complete HTML is not Loading using `Requests` because it's a Dynamic Website?

**Preferred) Use [Requests-HTML](https://docs.python-requests.org/projects/requests-html/en/latest) ([Alternative Link](https://requests.readthedocs.io/projects/requests-html/en/latest))**

- [How I Scrape JAVASCRIPT websites with Python](https://youtu.be/0hiGp3lF6ig) | [Scrape Amazon NEW METHOD with Python 2020](https://youtu.be/WcPNlnsNZyY)
- [Render Dynamic Pages - Web Scraping Product Links with Python](https://youtu.be/MeBU-4Xs2RU) | [Rendering Dynamic Pages 2! - Web Scraping ALL products with Python](https://youtu.be/B14mtXA7Tyw)
- [Python Tutorial: Web Scraping with Requests-HTML](https://youtu.be/a6fIbtFB46g)

**Alternative) Use [Selenium](https://www.selenium.dev/documentation)**

- [Scrape content from dynamic websites](https://www.geeksforgeeks.org/scrape-content-from-dynamic-websites)
- [How I use SELENIUM to AUTOMATE the Web with PYTHON. Pt1](https://youtu.be/pUUhvJvs-R4) | [How to SCRAPE DYNAMIC websites with Selenium](https://youtu.be/lTypMlVBFM4)

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
1) Download or Update the ChromeDriver binary for your platform from https://chromedriver.chromium.org/downloads
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

**Use [Threading](https://docs.python.org/3/library/threading.html)**

- [Python Threading Tutorial: Run Code Concurrently Using the Threading Module](https://youtu.be/IEEhzQoKtQU)
- [PARALLEL and CONCURRENCY in Python for FAST Web Scraping](https://youtu.be/aA6-ezS5dyY)

```py
from concurrent.futures import ThreadPoolExecutor

THREADS = 10

def main(i: int) -> None:
    print(i)

# Executing {THREADS} no. of threads at once:
with ThreadPoolExecutor() as Exec:
    Exec.map(main, range(1, THREADS+1))
```

**Want even more SPEED?**

- [How to Make 2500 HTTP Requests in 2 Seconds with Async & Await](https://youtu.be/Ii7x4mpIhIs)
- [multiprocessing vs multithreading vs asyncio in Python 3](https://stackoverflow.com/questions/27435284)


#### 6) Website have Rate Limit?

**Use [Proxies](https://en.wikipedia.org/wiki/Proxy_server)**

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


#### 7) Always send custom user agent (to tell the website that it's not a bot)

**Use [Custom Headers](https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers)**

- [User Agent Switching - Python Web Scraping](https://youtu.be/90t9WkQbQ2E)
- Get your user agent from: [Google](https://www.google.com/search?q=my+user+agent) or [httpbin.org](https://httpbin.org/user-agent)

```py
from requests import get as get_request

URL = 'https://httpbin.org/user-agent'

print('Without:', get_request(url=URL).json())
# Without: {'user-agent': 'python-requests/2.27.1'}

HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
print('With:', get_request(url=URL, headers=HEADER).json())
# With: {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'}
```


#### 8) Data to get is table data?

**Please use [`pandas.read_html`](https://pandasguide.readthedocs.io/en/latest)!!**

- [Scrape HTML tables easily with Pandas and Python](https://youtu.be/ODNMNwgtehk)


#### 9) [Always Check for the Hidden API when Web Scraping](https://youtu.be/DqtlR0y0suo) ([On Incognito] Inspect -> Network -> XHR -> Name -> some GET request -> Response)


#### 10) [Official `Beautiful Soup` Doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc)


#### 11) [Best Web Scraping Tutorials](https://www.youtube.com/c/JohnWatsonRooney/videos?sort=p)

#### 12) Data Storage Note: 

1. **Saving to large Excel files takes forever.** Never use Excel files to save large data, if required, partition it across multiple Excel files. See [this](8\)%20Bytecoin%20Explorer/Code.py#L31). *OR* Use CSV files instead!
2. **Excel = zipped(CSV).** If the data has to be saved across a large number of (small) files, use Excel files to end up taking very less storage in comparison with CSV files!


## Ciao!👋
