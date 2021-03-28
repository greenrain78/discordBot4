from typing import Tuple, Dict

import requests
from bs4 import BeautifulSoup


class StockCrawlingClient:

    @staticmethod
    def get_soup(company_code) -> BeautifulSoup:
        url = "https://finance.naver.com/item/main.nhn?code=" + company_code
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    @classmethod
    def get_price(cls, company_code):
        soup = cls.get_soup(company_code)
        result = cls.process_price(soup)
        return result

    @classmethod
    def get_stock_info(cls, company_code) -> Dict[str, str]:
        soup = cls.get_soup(company_code)
        result = {
            "now_price": cls.process_price(soup),
            "stock_name": cls.process_stock_name(soup)
        }
        return result

    @staticmethod
    def process_price(soup: BeautifulSoup):
        no_today = soup.find("p", {"class": "no_today"})
        blind = no_today.find("span", {"class": "blind"})
        now_price = blind.text
        return now_price

    @staticmethod
    def process_stock_name(soup: BeautifulSoup):
        result = soup.find("div", {"class": "wrap_company"})
        result = result.find("h2")
        result = result.text
        return result

    @classmethod
    def test_api(cls, company_code):
        soup = cls.get_soup(company_code)
        result = soup.find("div", {"class": "wrap_company"})
        result = result.find("h2")
        result = result.text
        return result
