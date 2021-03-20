import datetime
import matplotlib.pyplot as plt
import pandas_datareader as web
import numpy as np
import argparse
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def scrap_lowest(symbol, keyword, start_date, end_date):
    stock_df = web.DataReader(symbol, 'yahoo', start_date, end_date)
    stock_df['difference_crash'] = stock_df['Open'] - stock_df['Close']
    stock_df['difference_rise'] = stock_df['Close'] - stock_df['Open']
    row_crash = stock_df[stock_df['difference_crash']==stock_df['difference_crash'].max()]
    crash_date = row_crash.index.date[0]
    print(f'WORST DAY ({crash_date})')
    print("------------------------------------------------")
    scrap_google_news(keyword, crash_date)
    print("------------------------------------------------")
    row_rise = stock_df[stock_df['difference_rise']==stock_df['difference_rise'].max()]
    rise_date = row_rise.index.date[0]
    print(f'BEST DAY ({rise_date})')
    print("------------------------------------------------")
    scrap_google_news(keyword, rise_date)
    print("------------------------------------------------")


def scrap_google_news(search, search_date):
    options = webdriver.ChromeOptions()
    binary = '/usr/bin/chromium-browser'
    options.add_argument('headless')
    options.binary_location = binary 

    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    month = str(search_date.month)
    day = str(search_date.day)
    year = str(search_date.year)
    url = f'https://www.google.com/search?q={search}&biw=857&bih=985&sxsrf=ALeKk00U1s7feq1FWK1tSyHvfndjc1euZw%3A1616123558203&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{day}%2F{year}%2Ccd_max%3A{month}%2F{day}%2F{year}&tbm=nws'
    driver.get(url)
    sleep(1)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find_all('div', {"class":'JheGif nDgy9d'})
    for header in soup:
        title = header.text
        print(title)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="symbol letters of the company", type=str)
    parser.add_argument("keyword", help="keyword to search for those days", type=str)
    parser.add_argument('-s','--start_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="year-month-day", default=datetime.datetime(2015, 1,1))
    parser.add_argument('-e','--end_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="year-month-day", default=datetime.datetime.now())
    args = parser.parse_args()
    scrap_lowest(args.symbol, args.keyword, args.start_date, args.end_date)
