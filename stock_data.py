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