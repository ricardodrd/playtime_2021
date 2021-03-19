import requests
import argparse
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import serial

# CODES = {"yahoo": '', "euronext": 'NO0010776990'}

# euronext loads data dynamically using javascript
def scrap_data_euronext(url):
    options = webdriver.ChromeOptions()
    binary = '/usr/bin/chromium-browser'
    options.add_argument('headless')
    options.binary_location = binary 

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    driver.get(url)
    sleep(1)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('div', {"class": 'data-header__row bg-ui-yellow'})
    price = content.find_all('span')[1].text
    return price

def scrap_data_yahoo(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    soup = soup.find('div', {"class":'My(6px) Pos(r) smartphone_Mt(6px)'})
    price = soup.find_all('span')[0].text
    change = soup.find_all('span')[1].text
    bid_change = change.split(' ')[0]
    return price

def get_rt_data_yahoo(stock, step):
    # step is the number of seconds to wait between calls
    url = f'https://finance.yahoo.com/quote/{stock}?p={stock}&.tsrc=fin-srch'
    while True:
        print(scrap_data_yahoo(url)[1])
        sleep(step)

def get_both_real_data(symbol, isin, step):
    url_yahoo = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch'
    url_euronext = f'https://live.euronext.com/en/product/equities/{isin}-MERK/market-information'
    last_price = float(scrap_data_yahoo(url_yahoo))
    current_price = last_price
    alarm = False
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

    while True:
        current_price = float(scrap_data_yahoo(url_yahoo))
        print('yahoo:',current_price)
        alarm = evaluate_price(current_price, last_price, alarm, ser)
        sleep(step/2)
        current_price = float(scrap_data_euronext(url_euronext))
        print('euronext:', current_price)
        alarm = evaluate_price(current_price, last_price, alarm, ser)
        sleep(step/2)


def evaluate_price(current_price, last_price, alarm, ser):
    status = alarm
    if ((current_price > last_price) and alarm):
        ser.write('n'.encode())
        print('turn off light')
        status = False
    if ((current_price < last_price) and not alarm):
        print("turn on light")
        ser.write('l'.encode())
        status = True
    return status

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
    # get_rt_data_yahoo(args.symbol, args.step)
