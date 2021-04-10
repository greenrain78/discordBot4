from logging import getLogger
from typing import Optional

from DiscordBot4.DB import manageDB

log = getLogger(__name__)

tableName_stock = 'discord_stock'
tableName_history = 'discord_stock_history'

init_stock_DB = f"CREATE TABLE IF NOT EXISTS {tableName_stock}(" \
                f"no    INT NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
                f"user  VARCHAR(255)     NOT NULL, " \
                f"stock_name    VARCHAR(255) NOT NULL, " \
                f"code    VARCHAR(255) NOT NULL, " \
                f"price   INT     NOT NULL, " \
                f"quantity  INT    NOT NULL, " \
                f"time  datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP" \
                f");"

init_history_DB = f"CREATE TABLE IF NOT EXISTS {tableName_history}(" \
                  f"no      INT NOT NULL AUTO_INCREMENT PRIMARY KEY, " \
                  f"user   VARCHAR(255)     NOT NULL, " \
                  f"stock_name    VARCHAR(255) NOT NULL, " \
                  f"code    VARCHAR(255) NOT NULL, " \
                  f"price   INT     NOT NULL, " \
                  f"quantity  INT    NOT NULL, " \
                  f"reason  TEXT    NOT NULL, " \
                  f"time  datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP" \
                  f");"


class StockDB(object):

    @staticmethod
    def initDB():
        log.info("StockDB ")
        manageDB.runSQL(init_stock_DB)
        manageDB.runSQL(init_history_DB)

    @classmethod
    def buy_stock(cls, user: str, stock_name: str, code: str, price: int, quantity: int):
        now_quantity = cls.select_stock_quantity(user, code)
        if now_quantity is None:
            cls.insert_stock(user, stock_name, code,  price, quantity)
            reason = f"주식을 새로 구입하였습니다."
        else:
            cls.update_stock(user, code, price, quantity)
            reason = f"주식을 추가로 구입하였습니다."
        cls.insert_history(user, stock_name, code, price, quantity, reason)
        log.debug(
            f"buy_stock: user: {user}, code({code}), stock_name({stock_name}), price({price}), quantity({quantity})")

    @classmethod
    def sell_stock(cls, user: str, stock_name: str, code: str, price: int, quantity: int):
        now_quantity = cls.select_stock_quantity(user, code)
        if now_quantity - quantity > 0:
            cls.update_stock(user, code, price, -quantity)
            reason = f"주식을 {quantity}만큼 판매하였습니다."
        else:
            cls.delete_stock(user, code)
            reason = f"주식을 전량 매도하였습니다."
        cls.insert_history(user, stock_name, code, price, quantity, reason)
        log.debug(f"sell_stock: user: {user}, code({code}), price({price}), quantity({quantity})")

    @classmethod
    def retrieve_stock(cls, user: str):
        info = cls.select_stock_info(user)
        log.debug(f"retrieve_stock: user: {user} - %s", info)

        return info

    @classmethod
    def remains_stock(cls, user: str, code: str):
        remain = cls.select_stock_quantity(user, code)
        log.debug(f"retrieve_stock: user: {user}, code:{code} - %s", remain)
        return remain

    # ---------------------------------insert---------------------------------
    @staticmethod
    def insert_stock(user: str, stock_name: str, code: str, price: int, quantity: int):
        sql = f'insert into {tableName_stock} ' \
              f'(user, stock_name, code, price, quantity) values(' \
              f'"{user}","{stock_name}", "{code}", {price}, {quantity})'
        print(sql)
        manageDB.runSQL(sql)
        return sql

    # ---------------------------------update---------------------------------

    @staticmethod
    def update_stock(user: str, code: str, price: int, quantity: int):
        sql = f'update {tableName_stock} ' \
              f'SET quantity = quantity + {quantity}, ' \
              f'price = {price} ' \
              f'WHERE user = "{user}"  and code = "{code}"'
        manageDB.runSQL(sql)

    # ---------------------------------select---------------------------------

    @staticmethod
    def select_stock_quantity(user: str, code: str) -> Optional[int]:
        sql = f'select quantity from {tableName_stock} ' \
              f'WHERE user = "{user}"  and code = "{code}"'
        result = manageDB.getOneSQL(sql)
        log.debug("select_stock_quantity")
        if result:
            return result[0]
        else:
            return None

    @staticmethod
    def select_stock_info(user: str):
        sql = f'select * from {tableName_stock} ' \
              f'WHERE user = "{user}"'
        result = manageDB.getSQL(sql)
        log.debug("select_stock_info")
        return result

    @staticmethod
    def select_stock_list():
        sql = f'SELECT DISTINCT stock_name from {tableName_history} ' \
              f'ORDER BY time DESC '    # 최근순으로 정렬
        result = manageDB.getSQL(sql)
        log.debug("select_stock_code_list")
        return result

    # ---------------------------------delete---------------------------------

    @staticmethod
    def delete_stock(user: str, code: str):
        sql = f'DELETE from {tableName_stock} ' \
              f'WHERE user = "{user}" ' \
              f'and code = "{code}"'
        manageDB.runSQL(sql)

    # ---------------------------------history---------------------------------
    @staticmethod
    def insert_history(user: str, stock_name: str, code: str, price: int, quantity: int, reason: str):
        sql = f'insert into {tableName_history} ' \
              f'(user, stock_name, code, price, quantity, reason) values(' \
              f'"{user}", "{stock_name}", "{code}", {price}, {quantity}, "{reason}")'
        manageDB.runSQL(sql)
