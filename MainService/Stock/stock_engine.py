from datetime import datetime
from logging import getLogger
from typing import Union

import discord
from discord.embeds import Embed

from MainService.Point.point_DB import PointDB
from MainService.Stock.stock_DB import StockDB
from MainService.Stock.stock_crawling import StockCrawlingClient
from MainService.Stock.stock_graph import StockGraph

log = getLogger(__name__)


class StockEngine:
    StockDB.initDB()
    stock_list = StockCrawlingClient.get_all_stock_list()

    @classmethod
    def find_stock_code(cls, company: str) -> Union[bool, str]:
        # 주식 검색
        stock_code = cls.stock_list[cls.stock_list.company == company].code.values
        if not stock_code:
            return False
        else:
            stock_code = stock_code[0].strip()  # 주식 코드 가져오기, 공백 제거
            return stock_code

    @staticmethod
    def result_message(em: Embed, name):
        """
        :param em: 디코 메세지에
        :param name: 해당 유저의 주식 정보를
        :return: 추가한다.
        """
        title2 = f"유저: {name}의 보유 주식"
        text2 = ""
        stock_list = StockDB.retrieve_stock(name)
        if not stock_list:
            text2 += f"보유 주식이 없습니다."
        else:
            for stock in stock_list:
                pt_str = "{:,}".format(stock[4])
                text2 += f"주식명: {stock[2]} 코드: {stock[3]}\n" \
                         f"매수 금액: {pt_str}, 보유수: {stock[5]}, 시간{stock[6]}\n\n"
            em.add_field(name=title2, value=text2, inline=False)

    @classmethod
    def buy(cls, name, company, quantity) -> Embed:
        """
        :param name: 해당 유저가
        :param company: 해당 주식을
        :param quantity: 해당 갯수만큼
        :return: 구매하고 메세지를 전송
        """
        # 주식 검색
        stock_code = cls.find_stock_code(company)
        title = f"주식 검색: {company}"
        if not stock_code:
            text = f"해당 주식은 없습니다.\n" \
                   f"제대로 입력해 주세요"
            em = Embed(title=title, description=text)
            return em
        # 가격 조회
        price = StockCrawlingClient.get_now_price(stock_code)
        price = int(price.replace(',', ''))  # int 화

        # 보유 포인트 확인
        user_pt = PointDB.get_point(name)
        if price * quantity > user_pt:
            pt_str = "{:,}".format(user_pt)
            price_str = "{:,}".format(price)

            title = "주식 매수 실패"
            text = f"보유 포인트 부족으로 주식 매수를 실패하였습니다.\n" \
                   f"보유 포인트: {pt_str}, 주식 가격: {price_str}"
            em = Embed(title=title, description=text)
            footer = '돈 없으면 저리가'
            em.set_footer(text=footer)
            return em

        # DB 업데이트 - 포인트 감소, 주식 추가
        StockDB.buy_stock(name, company, stock_code, price, quantity)
        total = price * quantity * -1
        reason = f"{company} 주식({stock_code})를 {quantity}만큼 매수하였습니다."
        PointDB.earn_point_user(name, total, reason)

        # 메세지 생성
        title = "주식 매수 성공"
        text = f"해당 주식이 정상적으로 채결되었습니다."
        em = Embed(title=title, description=text)

        title1 = "매수 주식"
        text1 = f"주식명: {company}, 현재가: {price}, 채결 수량: {quantity}"
        em.add_field(name=title1, value=text1, inline=False)

        cls.result_message(em, name)
        return em

    @classmethod
    def sell(cls, name, company, quantity) -> Embed:
        # 주식 검색
        stock_code = cls.find_stock_code(company)
        title = f"주식 검색: {company}"
        if not stock_code:
            text = f"해당 주식은 없습니다.\n" \
                   f"제대로 입력해 주세요"
            em = Embed(title=title, description=text)
            return em
        # 보유 주식 확인
        stock_quantity = StockDB.remains_stock(name, stock_code)
        if not stock_quantity:
            title = "주식 매매 실패"
            text = f"해당 주식을 보유하고 있지 않습니다." \
                   f"입력하신 주식: {company}({stock_code})"
            em = Embed(title=title, description=text)
            footer = '주식도 없는 주제에 어딜'
            em.set_footer(text=footer)
            return em
        if quantity > stock_quantity:
            title = "주식 매매 실패"
            text = f"입력하신 수량이 보유 수량보다 많습니다." \
                   f"소유량: {stock_quantity}, 입력값: {quantity}"
            em = Embed(title=title, description=text)
            return em
        # 가격 조회
        price = StockCrawlingClient.get_now_price(stock_code)
        now_price = int(price.replace(',', ''))

        # DB 업데이트 - 포인트 증가, 주식 제거
        StockDB.sell_stock(name, company, stock_code, now_price, quantity)
        total = now_price * quantity
        reason = f"{company} 주식({stock_code})를 {quantity}만큼 판매하였습니다."
        PointDB.earn_point_user(name, total, reason)

        # 메세지 생성
        title = "주식 매매 성공"
        text = f"해당 주식이 정상적으로 채결되었습니다."
        em = Embed(title=title, description=text)

        title1 = "매매 주식"
        text1 = f"주식명: {company}, 현재가: {now_price}, 채결 수량: {quantity}"
        em.add_field(name=title1, value=text1, inline=False)

        cls.result_message(em, name)
        return em

    @classmethod
    def info(cls, name) -> Embed:
        user_stock_list = StockDB.retrieve_stock(name)
        title = f"{name}가 소유하고 있는 주식 리스트"
        log.debug(user_stock_list)
        if not user_stock_list:
            text = f"보유하고 계신 주식이 없습니다. "
            em = Embed(title=title, description=text)
            footer = '돈 없으면 저리가'
            em.set_footer(text=footer)
            return em

        text = f"아이구 어셥옵쇼"
        em = Embed(title=title, description=text)
        for stock in user_stock_list:
            now_price = StockCrawlingClient.get_now_price(stock[3])
            price_str = "{:,}".format(stock[4])

            title1 = f"주식명: {stock[2]}\n" \
                     f"코드: {stock[3]}"
            text1 = f"매수 금액: {price_str}\n" \
                    f"현재 금액: {now_price}\n" \
                    f"보유수: {stock[5]}\n" \
                    f"시간: {stock[6]}"
            em.add_field(name=title1, value=text1, inline=True)
        footer = '딜래이로 인해 실제와 많이 다를 수 있습니다.'
        em.set_footer(text=footer)
        return em

    @classmethod
    def search(cls, company: str, page_range):
        # 주식 검색
        stock_code = cls.find_stock_code(company)
        title = f"주식 검색: {company}"
        if not stock_code:
            text = f"해당 주식은 없습니다.\n" \
                   f"제대로 입력해 주세요"
            em = Embed(title=title, description=text)
            return em

        now_price = StockCrawlingClient.get_now_price(stock_code)
        text = f"주식코드: {stock_code}\n" \
               f"가격: {now_price}"
        em = Embed(title=title, description=text)

        # 파일 이름 설정
        str_time = str(datetime.now()).replace(' ', '_')
        str_time = str_time.replace('.', '-')
        str_time = str_time.replace(':', '-')
        file_name = f"media/stock_image/{company}_{str_time}" + ".png"

        # 그래프 생성
        stock_df = StockCrawlingClient.get_stock_list(stock_code, page_range=page_range)
        StockGraph.df_to_png(stock_df, file_name)
        print(" save png ")
        image = discord.File(file_name, filename="image.png")
        em.set_image(url="attachment://image.png")

        # 반환
        result = {
            "embed": em,
            "image": image,
        }
        return result

    @classmethod
    def popular(cls):
        title = f"최근 관심 주식 리스트"
        text = ""
        stock_list = StockDB.select_stock_list()
        for stock_name in stock_list:
            stock_name = stock_name[0]  # 이름 꺼내기

            stock_code = cls.find_stock_code(stock_name)
            price = StockCrawlingClient.get_now_price(stock_code)
            text += f"주식명: {stock_name}\n" \
                    f"코드: {stock_code}\n" \
                    f"가격: {price}\n\n"
        em = Embed(title=title, description=text)
        footer = '딜래이로 인해 실제와 많이 다를 수 있습니다.'

        em.set_footer(text=footer)
        return em

    @classmethod
    def stock_ramdom_list(cls, count):
        title = f"랜덤 주식 리스트"
        text = ""
        stock_list = cls.stock_list.sample(n=count)
        for stock in stock_list.itertuples():
            price = StockCrawlingClient.get_now_price(stock.code)
            text += f"주식명: {stock.company}\n" \
                    f"코드: {stock.code}\n" \
                    f"가격: {price}\n\n"
        em = Embed(title=title, description=text)
        footer = '딜래이로 인해 실제와 많이 다를 수 있습니다.'

        em.set_footer(text=footer)
        return em
