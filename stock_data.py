import datetime
import matplotlib.pyplot as plt
import pandas_datareader as web
import numpy as np
import argparse
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver

def compare_stocks(main_company, companies):
    start_date = datetime.datetime(2000, 1,1)
    end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    main_df = web.DataReader(main_company, 'yahoo', start_date, end_date)
    main_rows = main_df.shape[0]

    other_companies_dfs = [web.DataReader(company, 'yahoo', start_date, end_date).iloc[0:main_rows] 
                        for company in companies]
    all_companies_names = [main_company] + companies
    all_companies_dfs = [main_df] + other_companies_dfs

    for idx in range(0, len(all_companies_dfs)):
        company =all_companies_dfs[idx].reset_index() 
        company['Volume'].plot(label=all_companies_names[idx])
    plt.legend()
    plt.ylabel('Volume')
    plt.xlabel('Days')
    plt.show()

def scrap_lowest(symbol, company_name):
    start_date = datetime.datetime(2015, 1,1)
    end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_df = web.DataReader(symbol, 'yahoo', start_date, end_date)
    stock_df['difference_crash'] = stock_df['Open'] - stock_df['Close']
    stock_df['difference_rise'] = stock_df['Close'] - stock_df['Open']
    row_crash = stock_df[stock_df['difference_crash']==stock_df['difference_crash'].max()]
    crash_date = row_crash.index.date[0]
    print(f'WORST DAY ({crash_date})')
    print("------------------------------------------------")
    scrap_google(company_name, crash_date)
    print("------------------------------------------------")
    row_rise = stock_df[stock_df['difference_rise']==stock_df['difference_rise'].max()]
    rise_date = row_rise.index.date[0]
    print(f'BEST DAY ({rise_date})')
    print("------------------------------------------------")
    scrap_google(company_name, rise_date)
    print("------------------------------------------------")


def scrap_google(search, search_date):
    options = webdriver.ChromeOptions()
    binary = '/usr/bin/chromium-browser'
    options.add_argument('headless')
    options.binary_location = binary 

    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
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

def main(stock):
    start_date = datetime.datetime(2021, 1,1)
    end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stock_df = web.DataReader(stock, 'yahoo', start_date, end_date)
    stock_rows = stock_df.shape[0]

    # start_date_second_stock = datetime.datetime(2000, 1,1)
    # second_stock_df = web.DataReader('PEXIP.OL', 'yahoo', start_date, end_date)
    # second_stock_reduced_df = second_stock_df[]
    plot_cols(stock_df, ['Open', 'Close'])
    # plot_cols(stock_df, ['Volume'])

def plot_compare():
    print()

def plot_cols(df, cols):
    for col in cols:
        df[col].plot(label=col)
    plt.title('HUDDLY')
    plt.ylabel('PRICE')
    plt.legend()
    plt.locator_params(axis="x", nbins=16)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", help="symbol letters of the company", type=str)
    parser.add_argument("name", help="name of the company", type=str)
    parser.add_argument("-s", "--start", help="start_date", type=str)
    parser.add_argument("-e", "--end", help="end date", type=str)
    parser.add_argument('-c', '--companies', action='store',
                    type=str, nargs='*', default=None,
                    help="Examples: -i item1 item2, -i item3")
    args = parser.parse_args()
    # main(args.symbol)
    scrap_lowest(args.symbol, args.name)
    # compare_stocks(args.symbol, args.companies)