from datetime import datetime
from logging import getLogger
from typing import Optional

from DiscordBot4.DB import manageDB
from MainService.ERBS.erbs_sql import init_games_DB, init_stats_DB, tableName_games, game_data_type

log = getLogger(__name__)


class ErbsDB(object):

    @staticmethod
    def initDB():
        log.info("ErbsDB ")
        manageDB.runSQL(init_games_DB)
        manageDB.runSQL(init_stats_DB)

    @classmethod
    def insert_games(cls, data: dict):
        log.info("ErbsDB insert_games %s", data)
        sql_header = f'insert into {tableName_games} ('
        sql_column = f''
        sql_values = f') values('
        for col, val in data.items():
            # 해당 컬럼이 없나?
            if col not in game_data_type.keys():
                log.error("ErbsDB does not have columns %s", col)
            else:
                sql_column += f'{col} ,'
                # 타입별로 변환
                if col == "startDtm":
                    val = val.translate({ord('T'): ' '})
                    val = val[:-5]
                    val = datetime.strptime(val, '%Y-%m-%d %H:%M:%S.%f')
                    log.debug(f"test: {val}")
                    sql_values += f'"{val}", '

                elif game_data_type[col] == "JSON":
                    data_str = f'{val}'
                    data_str = data_str.replace('\'', "\"")
                    sql_values += f"'{data_str}', "

                elif type(val) == int or type(val) == float:
                    sql_values += f'{val}, '
                else:
                    sql_values += f'"{val}", '

        # , 제거
        sql_column = sql_column[:-2]
        sql_values = sql_values[:-2]

        sql = sql_header + sql_column + sql_values + ")"
        manageDB.runSQL(sql)

    @staticmethod
    def isExistData(userNum, gameId) -> bool:
        sql = f'select no from {tableName_games} ' \
              f'WHERE userNum = "{userNum}"  and gameId = "{gameId}"'
        result = manageDB.getOneSQL(sql)
        log.debug("ErbsDB isExistData")

        if result:
            return True
        else:
            return False
