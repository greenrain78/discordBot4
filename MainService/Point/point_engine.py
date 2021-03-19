from logging import getLogger
import discord
from discord.embeds import Embed
from apscheduler.schedulers.background import BackgroundScheduler
from MainService.Point.point_DB import PointDB
from settings import debug

log = getLogger(__name__)

point_table = {
    'first': 500,
    'sleep': 20,
    'daily': 100,
}


class PointEngine:
    sleep_list = {}
    schedule = BackgroundScheduler()

    def __init__(self):
        # 초기화
        self.sleepList = None
        PointDB.initDB()
        self.initUserList()
        # 스캐줄 생성
        self.schedule.start()
        if not debug:
            self.schedule.add_job(self.dailyReset, 'cron', hour=12, id="dailyReset")
        else:
            self.schedule.add_job(self.dailyReset, 'cron', second=40, id="dailyReset")
        log.info("PointEngine init")

    @staticmethod
    def eventInfo() -> Embed:
        title = "디스코드 포인트 이벤트"
        text = '디스코드 포인트를 모아 기프티콘을 받아 가자!!!!'
        em = discord.Embed(title=title, description=text)

        title1 = "포인트 획득 방법"
        text1 = f"1. 매일 꾸준히 디스코드 방에 접속하여 출석채크를 한다.\n" \
                f"2. 도박 기능 출시 예정\n"
        em.add_field(name=title1, value=text1, inline=False)

        title2 = "상품 목록"
        text2 = f"커피 기프티콘 2장\n" \
                f"목표 포인트: 10000pt\n" \
                f"남은 수량: 0장\n" \
                f"(상일이가 모든 상품을 수령하였습니다.)\n\n" \
                f"아직 상품이 준비안되었습니다.\n" \
                f"프리 시즌 기간"

        em.add_field(name=title2, value=text2, inline=False)

        footer = '반응이 좋거나 활성화가 잘되면 상품을 더 늘리겠습니다.'
        em.set_footer(text=footer)
        return em

    def getPoint(self, name: str) -> str:
        if name not in self.sleep_list:
            text = f"미등록 사용자 입니다."
            return text
        pt = PointDB.get_point(name)
        text = f'유저({name})의 획득 포인트는 {pt}입니다,'
        return text

    def dailyReset(self):
        for user in self.sleep_list:
            self.sleep_list[user] = self.sleep_list[user] + 1
            PointDB.update_sleep_user(user, self.sleep_list[user])
        log.info("daily user reset: %s", self.sleep_list)

    def dailyCheck(self, name):
        # 최초 채팅 -> 리스트 추가
        if name not in self.sleep_list:
            PointDB.create_user(name, "new user", 0, 0)
            PointDB.earn_point_user(name, point_table['first'], "처음으로 출석하셨습니다.")

            self.initUserList()
            text = f"{name}님이 최초로 채팅을 하셨습니다. ㅊㅋㅊㅋ\n" \
                   f"특별 보너스로 {point_table['first']}포인트 적립되었습니다."
            return text

        # 오늘 처음 채팅 -> 포인트 획득
        if self.sleep_list[name] != 0:
            # 개근 여부 확인
            if self.sleep_list[name] == 1:
                get_point = point_table['daily']
                text = f"{name}이 출석하여 {point_table['daily']}포인트를 획득하셨습니다."
                reason = "출석채크로 포인트 획득"
            else:
                get_point = point_table['daily'] + point_table["sleep"] * self.sleep_list[name]
                text = f"{name}이 {self.sleep_list[name]}일만에 복귀했습니다.\n" \
                       f"특별 보너스 포인트로 {get_point}포인트를 획득하셨습니다."
                reason = "휴면계정을 복구하셔서 보너스 포인트"

            # 포인트 획득
            PointDB.earn_point_user(name, get_point, reason)
            self.sleep_list[name] = 0
            return text
        else:
            # 중복 채팅 -> 무시
            return None

    def initUserList(self):
        # make user list
        tmp_sleepList = PointDB.get_sleepList()
        if tmp_sleepList:
            self.sleep_list = {user[0]: user[1] for user in tmp_sleepList}
            log.debug("bot init sleepList: %s", self.sleep_list)
