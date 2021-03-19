import requests
import argparse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

# CODES = {"yahoo": '', "euronext": 'NO0010776990'}

# euronext loads data dynamically using javascript
def scrap_data_euronext(url):
    options = webdriver.ChromeOptions()
    binary = '/usr/bin/chromium-browser'
    options.add_argument('headless')
    options.binary_location = binary 

    driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('div', {"class": 'data-header__row bg-ui-yellow'})
    price = content.find_all('span')[1].text
    return price

def scrap_data_yahoo(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    soup = soup.find('div', {"class":'My(6px) Pos(r) smartphone_Mt(6px)'})
    price = soup.find('span').text
    return price

def get_rt_data_yahoo(stock, step):
    # step is the number of seconds to wait between calls
    url = f'https://finance.yahoo.com/quote/{stock}?p={stock}&.tsrc=fin-srch'
    print(url)
    while True:
        print(scrap_data_yahoo(url))
        sleep(step)

def get_both_real_data(symbol, isin, step):
    url_yahoo = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch'
    url_euronext = f'https://live.euronext.com/en/product/equities/{isin}-MERK/market-information'
    while True:
        print(scrap_data_yahoo(url_yahoo))
        sleep(step/2)
        print(scrap_data_euronext(url_euronext))
        sleep(step/2)


def get_rt_data_euronext(isin_code, step):
    url = f'https://live.euronext.com/en/product/equities/NO0010776990-MERK/market-information'
    while True:
        print(scrap_data_euronext(url))
        sleep(step)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="symbol letters of the company", type=str)
    parser.add_argument("isin", help="isin code of the company", type=str)
    parser.add_argument("-s", "--step", help="symbol letters of the company", type=int, default=20)
    args = parser.parse_args()
    # get_rt_data_euronext(args.symbol, args.step)
    get_both_real_data(args.symbol, args.isin, args.step)    