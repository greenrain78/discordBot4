import time

import pandas as pd
import pybithumb

from MainService.Stock.coin_api import CoinCrawlingClient
from MainService.Stock.stock_crawling import StockCrawlingClient


import requests
from bs4 import BeautifulSoup
# result = CoinCrawlingClient.get_now_price("BTC")
# print(result)
# #
#
#
tickers = pybithumb.get_tickers()
for ticker in tickers:
    price = pybithumb.get_current_price(ticker)
    print(ticker, price)
    print(int(price))
# company_list = []
# code_list = []
# for coin in tickers:
#     coin = coin.lower()
#     code_list.append(coin)
#
#     url = "https://www.coinhills.com/ko/market/" + coin
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'lxml')
#     no_today = soup.find("h1")
#     coin_str = no_today.text
#     coin_str = coin_str.replace(" 마켓", "")
#     company_list.append(coin_str)
#
# coin_list = pd.DataFrame({
#     'company': company_list,
#     'code': code_list,
# })
# print(coin_list)
#
# stock_list = StockCrawlingClient.get_all_stock_list()
# result2 = pd.concat([coin_list, stock_list], ignore_index=True)
#
# print(type(result2))
# print(result2)
#
#
# price = CoinCrawlingClient.get_now_price('BTC')
# print(type(price))
# print(price)
