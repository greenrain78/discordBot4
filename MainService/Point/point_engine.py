import random
from datetime import datetime, timedelta
from logging import getLogger
import discord
from discord.embeds import Embed
from apscheduler.schedulers.background import BackgroundScheduler
from MainService.Point.point_DB import PointDB
from settings import debug

log = getLogger(__name__)

point_table = {
    'first': 50000,
    'sleep': 2000,
    'daily': 10000,
}
random_box_time = timedelta(days=1)
random_max_point = 10000
random_min_point = 1


class PointEngine:
    sleep_list = {}
    box_list = {}
    schedule = BackgroundScheduler()
    PointDB.initDB()

    def __init__(self):
        log.info("PointEngine init 실제 동작 안함")

    @classmethod
    def initSchedule(cls):
        # 초기화
        cls.initUserList()
        # 스캐줄 생성
        cls.schedule.start()
        if not debug:
            cls.schedule.add_job(cls.dailyReset, 'cron', hour=12, id="dailyReset")
        else:
            cls.schedule.add_job(cls.dailyReset, 'cron', second=40, id="dailyReset")
        log.info("PointEngine init schedule")

    @staticmethod
    def event_info() -> Embed:
        title = "디스코드 포인트 이벤트"
        text = '내 집 아니 내 치킨 마련!!'
        em = discord.Embed(title=title, description=text)

        title1 = "포인트 획득 방법"
        text1 = f"1. 매일 꾸준히 디스코드 방에 접속하여 출석채크를 한다.\n" \
                f"2. 자신만의 투자 비법으로 주식 투자. ($stcok)\n" \
                f"3. 친구들과 내기를 통해 친구 등쳐먹기 ($bet)\n" \
                f"4. 인생은 운빨, 각종 게임으로 내 운을 시험해 본다. ($game)"
        em.add_field(name=title1, value=text1, inline=False)

        title2 = "상품 목록"
        text2 = f"파인다이닝 런치\n" \
                f"목표 포인트: 1억 pt\n" \
                f"수량: 1장 \n\n" \
                f"치킨 기프티콘 1장\n" \
                f"목표 포인트: 3천만원 pt\n" \
                f"수량: 2장 \n\n"
        em.add_field(name=title2, value=text2, inline=False)
        title3 = "역대 상품 목록"
        text3 = f"1. 커피 기프티콘 2장 - 모두 상일이가 수령"

        em.add_field(name=title3, value=text3, inline=False)
        footer = '여러분의 후원이 더 좋은 콘텐츠를 만듭니다.'
        em.set_footer(text=footer)
        return em

    @classmethod
    def get_point(cls, name: str) -> str:
        if name not in cls.sleep_list:
            text = f"미등록 사용자 입니다."
            return text
        pt = PointDB.get_point(name)
        pt_str = "{:,}".format(pt)
        text = f'유저({name})의 획득 포인트는 {pt_str}입니다,'
        return text

    @classmethod
    def get_list(cls, name: str) -> str:
        response = PointDB.get_list(name)
        title = f"사용자: {name}의 점수 리스트"
        text = ""
        for row in response:
            pt_str = "{:,}".format(row[2])
            text += f"{pt_str} pt : " \
                    f"날짜({row[4]}), " \
                    f"총합({row[5]}) \n" \
                    f"{row[3]}\n\n"

        em = discord.Embed(title=title, description=text)
        return em

    @classmethod
    def give_point(cls, name: str, point: int) -> str:
        if name not in cls.sleep_list:
            text = f"미등록 사용자 입니다."
            return text
        reason = f"관리자에 의해 사용자({name})가 포인트를 {point}만큼 획득하였습니다."
        PointDB.earn_point_user(name, point, reason)
        pt = PointDB.get_point(name)
        text = f"관리자에 의해 사용자({name})가 포인트를 획득하셨습니다." \
               f"획득 포인트: {point}, 총 포인트: {pt}"
        return text

    @classmethod
    def dailyReset(cls):
        for user in cls.sleep_list:
            cls.sleep_list[user] = cls.sleep_list[user] + 1
            PointDB.update_sleep_user(user, cls.sleep_list[user])
        log.info("daily user reset: %s", cls.sleep_list)

    @classmethod
    def dailyCheck(cls, name):
        # 최초 채팅 -> 리스트 추가
        if name not in cls.sleep_list:
            PointDB.create_user(name, "new user", point_table['first'])

            cls.initUserList()
            text = f"{name}님이 최초로 채팅을 하셨습니다. ㅊㅋㅊㅋ\n" \
                   f"특별 보너스로 {point_table['first']}포인트 적립되었습니다."
            return text

        # 오늘 처음 채팅 -> 포인트 획득
        if cls.sleep_list[name] != 0:
            # 개근 여부 확인
            if cls.sleep_list[name] == 1:
                get_point = point_table['daily']
                text = f"{name}이 출석하여 {point_table['daily']}포인트를 획득하셨습니다."
                reason = "출석채크로 포인트 획득"
            else:
                get_point = point_table['daily'] + point_table["sleep"] * cls.sleep_list[name]
                text = f"{name}이 {cls.sleep_list[name]}일만에 복귀했습니다.\n" \
                       f"특별 보너스 포인트로 {get_point}포인트를 획득하셨습니다."
                reason = "휴면계정을 복구하셔서 보너스 포인트"

            # 포인트 획득
            PointDB.earn_point_user(name, get_point, reason)
            cls.sleep_list[name] = 0
            return text
        else:
            # 중복 채팅 -> 무시
            return None

    @classmethod
    def initUserList(cls):
        # make user list
        tmp_sleepList = PointDB.get_sleepList()
        if tmp_sleepList:
            cls.sleep_list = {user[0]: user[1] for user in tmp_sleepList}
            log.debug("bot init sleepList: %s", cls.sleep_list)

    @classmethod
    def random_box(cls, user, betting):

        # 처음 받음
        if user not in cls.box_list:
            # 새로 추가
            cls.box_list[user] = datetime.now()
            # 랜덤 박스 열기
            em = cls.open_random_box(user, betting)
            return em

        remains_time = datetime.now() - cls.box_list[user]
        # 이미 받음
        if remains_time < random_box_time:
            title = "랜덤 박스를 열 수 없습니다."
            text = f'이미 받았잖아!!!\n' \
                   f'남은 시간: {random_box_time - remains_time}'
            em = discord.Embed(title=title, description=text)
            return em
        else:
            # 처음은 아니지만 갱신
            cls.box_list[user] = datetime.now()
            # 랜덤 박스 열기
            em = cls.open_random_box(user, betting)
            return em

    @classmethod
    def open_random_box(cls, user, betting) -> Embed:
        # 포인트 계산
        rand_point = random.randrange(random_min_point, random_max_point)
        get_point = rand_point + rand_point * (betting/random_max_point)
        # 포인트 입력
        reason = f"일일 랜덤 박스로 포인트 {get_point} 획득"
        PointDB.earn_point_user(user, get_point, reason)

        # 메세지 작성
        now_pt = PointDB.get_point(user)
        title = "랜덤 박스를 열었습니다"
        text = f'{user}가 {get_point}pt 획득\n' \
               f'총 {now_pt}pt 보유중'
        em = discord.Embed(title=title, description=text)
        return em

    @classmethod
    def ranking(cls):
        title = "포인트 랭킹"
        ranking_list = PointDB.get_ranking_List()
        text = f"이미 있었지만 아무도 안보는 것 같아서 따로 만드는 랭킹"
        em = Embed(title=title, description=text)
        for user in ranking_list:
            title1 = f"{user[0]}"
            text1 = f"{user[1]}pt"
            em.add_field(name=title1, value=text1, inline=False)
        return em
