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
    sleep(3)
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
    latest = 'euronext'
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

    while True:
        yahoos_current_price = float(scrap_data_yahoo(url_yahoo))
        sleep(1)
        euronex_current_price = float(scrap_data_euronext(url_euronext))
        print('yahoo:',yahoos_current_price,'euronext:', euronex_current_price)
        # alarm, current_price, latest = evaluate_price(yahoos_current_price, euronex_current_price, latest, last_price, alarm, ser)
        alarm = evaluate_price(yahoos_current_price, last_price, alarm, ser)
        last_price = yahoos_current_price
        print('Latest price',last_price)
        sleep(step/2)


def evaluate_price(current_yahoo, last_price, alarm, ser):
    status = alarm
    # if (current_yahoo != current_euronext):
    #     if (current_yahoo != last_price and current_euronext != last_price):
    #         current_price = current_euronext
    #         latest = 'euronext'
    #     else:
    #         if latest == 'euronext':
    #             if(current_euronext != last_price):
    #                 current_price = current_yahoo
    #                 latest = 'yahoo'
    #             else: 
    #                 current_price = current_euronext
    #         else:
    #             if(current_euronext != last_price):
    #                 current_price = current_euronext
    #                 latest = 'euroext'
    #             else:
    #                 current_price = current_yahoo
    # else:
    #     current_price = current_euronext

    if ((current_yahoo > last_price) and alarm):
        ser.write('n'.encode())
        print('Price goes up. Turn off light')
        status = False
    if ((current_yahoo < last_price) and not alarm):
        print("Price goes down. Turn on light")
        ser.write('l'.encode())
        status = True
    
    return status

def scrap_google(search):
    options = webdriver.ChromeOptions()
    binary = '/usr/bin/chromium-browser'
    options.add_argument('headless')
    options.binary_location = binary 

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    month = '2'
    day = '1'
    year = '2021'
    url = f'https://www.google.com/search?q={search}&biw=857&bih=985&sxsrf=ALeKk00U1s7feq1FWK1tSyHvfndjc1euZw%3A1616123558203&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{day}%2F{year}%2Ccd_max%3A{month}%2F{day}%2F{year}&tbm=nws'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find_all('div', {"class":'JheGif nDgy9d'})
    for header in soup:
        title = header.text
        print(title)
        print()


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
    # scrap_google(args.symbol)
    # get_rt_data_yahoo(args.symbol, args.step)
