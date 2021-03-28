from logging import getLogger

from discord.embeds import Embed

from MainService.Point.point_DB import PointDB
from MainService.Stock.stock_DB import StockDB
from MainService.Stock.stock_crawling import StockCrawlingClient

log = getLogger(__name__)


class StockEngine:
    StockDB.initDB()

    @staticmethod
    def result_message(em: Embed, name):
        title2 = f"유저: {name}의 보유 주식"
        text2 = ""
        stock_list = StockDB.retrieve_stock(name)
        if not stock_list:
            text2 += f"보유 주식이 없습니다."
        else:
            for stock in stock_list:
                text2 += f"주식명: {stock[2]} 코드: {stock[3]}\n" \
                         f"매수 금액: {stock[4]}, 보유수: {stock[5]}, 시간{stock[6]}\n\n"
            em.add_field(name=title2, value=text2, inline=False)
        # return em

    @classmethod
    def buy(cls, name, code, quantity) -> Embed:
        # 가격 조회
        # To do 추후에 try 문으로 예외처리
        stock_info = StockCrawlingClient.get_stock_info(code)
        price = int(stock_info["now_price"].replace(',', ''))

        # 보유 포인트 확인
        pt = PointDB.get_point(name)
        if price > pt:
            title = "주식 매수 실패"
            text = f"보유 포인트 부족으로 주식 매수를 실패하였습니다.\n" \
                   f"보유 포인트: {pt}, 주식 가격: {price}"
            em = Embed(title=title, description=text)
            footer = '돈 없으면 저리가'
            em.set_footer(text=footer)
            return em

        # DB 업데이트 - 포인트 감소, 주식 추가
        StockDB.buy_stock(name, stock_info["stock_name"], code, price, quantity)
        total = price * quantity * -1
        reason = f"{stock_info['stock_name']} 주식({code})를 {quantity}만큼 매수하였습니다."
        PointDB.earn_point_user(name, total, reason)

        # 메세지 생성
        title = "주식 매수 성공"
        text = f"해당 주식이 정상적으로 채결되었습니다."
        em = Embed(title=title, description=text)

        title1 = "매수 주식"
        text1 = f"주식명: {stock_info['stock_name']}, 현재가: {price}, 채결 수량: {quantity}"
        em.add_field(name=title1, value=text1, inline=False)

        cls.result_message(em, name)
        return em

    @classmethod
    def sell(cls, name, code, quantity) -> Embed:
        # 보유 주식 확인
        stock_quantity = StockDB.remains_stock(name, code)
        if not stock_quantity:
            title = "주식 매매 실패"
            text = f"해당 주식을 보유하고 있지 않습니다." \
                   f"입력하신 주식 코드: {code}"
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
        stock_info = StockCrawlingClient.get_stock_info(code)
        now_price = int(stock_info["now_price"].replace(',', ''))

        # DB 업데이트 - 포인트 증가, 주식 제거
        StockDB.sell_stock(name, stock_info['stock_name'], code, now_price, quantity)
        total = now_price * quantity
        reason = f"{stock_info['stock_name']} 주식({code})를 {quantity}만큼 판매하였습니다."
        PointDB.earn_point_user(name, total, reason)

        # 메세지 생성
        title = "주식 매매 성공"
        text = f"해당 주식이 정상적으로 채결되었습니다."
        em = Embed(title=title, description=text)

        title1 = "매매 주식"
        text1 = f"주식명: {stock_info['stock_name']}, 현재가: {now_price}, 채결 수량: {quantity}"
        em.add_field(name=title1, value=text1, inline=False)

        cls.result_message(em, name)
        return em

    @classmethod
    def info(cls, name) -> Embed:
        stock_list = StockDB.retrieve_stock(name)
        title = f"{name}가 소유하고 있는 주식 리스트"
        log.debug(stock_list)
        if stock_list:
            text = f" test"
            em = Embed(title=title, description=text)
            for stock in stock_list:
                title1 = f"주식명: {stock[2]} 코드: {stock[3]}"
                text1 = f"매수 금액: {stock[4]}, 보유수: {stock[5]}, 시간{stock[6]}"
                em.add_field(name=title1, value=text1, inline=True)
            footer = '딜래이로 인해 실제와 많이 다를 수 있습니다.'
        else:
            text = f"보유하고 계신 주식이 없습니다. "
            em = Embed(title=title, description=text)
            footer = '돈 없으면 저리가'
        em.set_footer(text=footer)
        return em

    @classmethod
    def search(cls, code: str):
        title = f"주식 검색: 코드 - {code}"
        response = StockCrawlingClient.get_stock_info(code)
        text = f"주식명: {response['stock_name']}" \
               f"가격: {response['now_price']}"
        em = Embed(title=title, description=text)
        footer = '딜래이로 인해 실제와 많이 다를 수 있습니다.'

        em.set_footer(text=footer)
        return em

    @classmethod
    def popular(cls, name):
        pass
