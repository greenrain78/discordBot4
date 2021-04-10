from typing import Tuple, Dict
from urllib.request import urlopen

import pandas
import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame


class StockCrawlingClient:
    header = {'User-Agent': 'Mozilla/5.0'}

    @staticmethod
    def get_all_stock_list() -> DataFrame:
        # 한국거래소에서 상장법인목록을 엑셀로 다운로드하는 링크
        stock_code = pandas.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

        # 회사명과 종목코드만 가져오기
        stock_code = stock_code[['회사명', '종목코드']]

        # 한글 컬럼명을 영어로 변경
        stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})

        # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
        stock_code.code = stock_code.code.map('{:06d}'.format)
        return stock_code

    @classmethod
    def get_stock_list(cls, code, page_range: int):
        df = pandas.DataFrame()
        for page in range(1, page_range):
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}"
            res = requests.get(url, headers=cls.header)
            df = df.append(pandas.read_html(res.text, header=0)[0], ignore_index=True)
        df = df.dropna()  # 빈 데이터 제거

        # 한글로 된 컬럼명을 영어로 바꿔줌
        df = df.rename(columns={
            '날짜': 'date',
            '종가': 'close',
            '전일비': 'diff',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '거래량': 'volume'})
        # 데이터의 타입을 int형으로 바꿔줌
        df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[
            ['close', 'diff', 'open', 'high', 'low', 'volume']].astype(
            int)

        # 컬럼명 'date'의 타입을 date로 바꿔줌
        df['date'] = pandas.to_datetime(df['date'])

        # 일자(date)를 기준으로 오름차순 정렬
        df = df.sort_values(by=['date'], ascending=True)
        return df

    @classmethod
    def get_now_price(cls, company_code):
        url = "https://finance.naver.com/item/main.nhn?code=" + company_code
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        no_today = soup.find("p", {"class": "no_today"})
        blind = no_today.find("span", {"class": "blind"})
        now_price = blind.text
        return now_price

    @classmethod
    def get_world_stock_info(cls, company_code) -> Dict[str, str]:
        url = "https://m.stock.naver.com/index.html#/worldstock/stock/" + company_code
        print(url)
        res = requests.get(url, headers=cls.header)
        print(res)
        soup = BeautifulSoup(res.text, 'lxml')
        print(soup)
        now_price = soup.find("strong", {"class": "GraphMain_price__u2XyL"})
        return now_price
