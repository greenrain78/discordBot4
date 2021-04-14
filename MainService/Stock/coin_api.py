import pandas as pd
import pybithumb
import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame


class CoinCrawlingClient:

    @staticmethod
    def get_all_stock_list() -> DataFrame:
        # 모든 티커 가져오기
        tickers = pybithumb.get_tickers()

        company_list = []
        code_list = []
        # 코인 이름 알아오기
        for coin in tickers:
            # 코인 코드 추가
            code_list.append(coin)
            # 크롤링
            url = "https://www.coinhills.com/ko/market/" +  coin.lower()
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            no_today = soup.find("h1")

            # 데이터 가공
            coin_str = no_today.text
            coin_str = coin_str.replace(" 마켓", "")
            company_list.append(coin_str)

        # 데이터 프레임 생성
        coin_list = pd.DataFrame({
            'company': company_list,
            'code': code_list,
        })
        return coin_list

    @classmethod
    def get_coin_list(cls, code: str, page_range: int):
        df = pybithumb.get_ohlcv(code)
        result = df.iloc[page_range:]
        return result

    @classmethod
    def get_now_price(cls, ticker: str) -> int:
        price = pybithumb.get_current_price(ticker)
        print(price)
        price = int(price)
        return price
