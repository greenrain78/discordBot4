from logging import getLogger
from typing import List

from DiscordBot4.DB import manageDB

log = getLogger(__name__)

tableName_user = 'discord_user'
tableName_point = 'discord_point'

init_user_DB = f'CREATE TABLE IF NOT EXISTS {tableName_user}(' \
               f'no      INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ' \
               f'name    VARCHAR(255) NOT NULL, ' \
               f'role    VARCHAR(255) NOT NULL, ' \
               f'join_time  datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP, ' \
               f'point   INT     NOT NULL, ' \
               f'sleep   INT     NOT NULL, ' \
               f'game_count   INT DEFAULT 0' \
               f');'

init_point_DB = f"CREATE TABLE IF NOT EXISTS {tableName_point}(" \
                f"no      INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                f"user    VARCHAR(255) NOT NULL," \
                f"point   INT     NOT NULL," \
                f"reason  TEXT    NOT NULL," \
                f"time  datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                f"total   INT     NOT NULL" \
                f");"


class PointDB(object):

    @staticmethod
    def initDB():
        log.info("PointDB ")
        manageDB.runSQL(init_user_DB)
        manageDB.runSQL(init_point_DB)

# ---------------------------------create---------------------------------

    @staticmethod
    def create_user(name: str, role: str, point: int):
        sql = f'insert into {tableName_user} ' \
              f'(name, role, point, sleep) values(' \
              f'"{name}", "{role}", {point}, {0})'
        manageDB.runSQL(sql)

        PointDB.earn_point_user(name, point, "처음으로 출석하셨습니다.")
        log.debug(f"insert_user: {name}, role({role}), point({point})")

# ---------------------------------update---------------------------------

    @staticmethod
    def earn_point_user(user: str, point: int, reason: str):
        # 포인트 조회
        prev_point = PointDB.get_point(user)
        # 기록 저장
        total = prev_point+point
        point_sql = f'insert into {tableName_point} ' \
                    f'(user, point, reason, total) values(' \
                    f'"{user}", {point}, "{reason}", {total})'
        manageDB.runSQL(point_sql)
        # 포인트 정보 갱신
        user_sql = f'UPDATE {tableName_user} ' \
                   f'SET point = {total} ' \
                   f'WHERE name = "{user}"'
        manageDB.runSQL(user_sql)
        # 포인트 획득했으니 awake
        PointDB.update_sleep_user(user, 0)
        log.debug(f"{user} insert point({point}), total({total}), reason({reason})")

    @staticmethod
    def update_sleep_user(name: str, sleep: int):
        sql = f'UPDATE {tableName_user} ' \
              f'SET sleep = {sleep} ' \
              f'WHERE name = "{name}"'

        manageDB.runSQL(sql)
        log.debug(f"update user({name}): sleep({sleep})")

    @staticmethod
    def update_game_count_user(name: str):
        sql = f'UPDATE {tableName_user} ' \
              f'SET game_count = game_count + 1 ' \
              f'WHERE name = "{name}"'

        manageDB.runSQL(sql)
        log.debug(f"update user({name}): wake up ")

# ---------------------------------select---------------------------------

    @staticmethod
    def get_point(user: str) -> int:
        sql = f'select point from {tableName_user} ' \
              f'WHERE name = "{user}"'
        result = manageDB.getOneSQL(sql)
        log.debug("get_point")
        return result[0]

    @staticmethod
    def get_list(user: str) -> List:
        sql = f'SELECT * FROM {tableName_point} ' \
              f'WHERE user = "{user}" ' \
              f'ORDER BY time DESC LIMIT 10;'
        result = manageDB.getSQL(sql)
        log.debug(f"read user list = {user} : {result} ")
        return result

    @staticmethod
    def get_sleepList() -> List[tuple]:
        sql = f"select name, sleep from {tableName_user}"
        result = manageDB.getSQL(sql)
        log.debug("get_sleepList")
        return result








