import time
from logging import getLogger

from apscheduler.schedulers.background import BackgroundScheduler

from MainService.ERBS.ERBS_api_client import ErbsClient
from MainService.ERBS.erbs_DB import ErbsDB
from settings import erbs_api_key

log = getLogger(__name__)


class ErbsScheduler(object):
    """
    1. 매일매일 유저 경기 내역 갱신
    2. DB 에서 데이터 가져오기
    """
    erbsAPI = ErbsClient(api_key=erbs_api_key, version='v1')
    schedule = BackgroundScheduler()
    user_list = [105103, 99148, 1933224, 99159]

    @classmethod
    def init_schedule(cls):
        cls.schedule.start()
        # cls.schedule.add_job(cls.update_erbs_DB, 'cron', second=10, id="update_erbs_DB")
        cls.schedule.add_job(cls.update_erbs_DB, 'cron', hour=12, id="update_erbs_DB")

        log.info("ErbsScheduler init_schedule ")

    @classmethod
    def update_erbs_DB(cls):
        log.info("ErbsScheduler get_all_games ")
        # 한명씩 차례대로
        for user_num in cls.user_list:
            cls.get_all_games(user_num)

    @classmethod
    def get_all_games(cls, user_num):
        nextNum = None
        while True:
            response = cls.erbsAPI.fetch_user_games_next(user_num, next=nextNum)
            nextNum = response['next']
            # 1판씩 저장
            log.info("ErbsScheduler get_all_games  - %s", response)
            for game in response['games']:
                # 중복 검사
                if ErbsDB.isExistData(userNum=game['userNum'], gameId=game['gameId']):
                    nextNum = None
                    break
                # 데이터 삽입
                ErbsDB.insert_games(game)
            if not nextNum:
                break
            # 딜레이 1초
            time.sleep(1)
