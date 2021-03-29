from datetime import datetime
from logging import getLogger

from discord.embeds import Embed

from MainService.Point.point_engine import PointEngine

log = getLogger(__name__)


class BasicEngine:
    startTime = datetime.now()

    def __init__(self):
        log.info("BasicEngine init 실제 동작 안함")

    @classmethod
    def get_state(cls) -> Embed:
        sleepList = PointEngine.sleep_list
        runningTime = datetime.now() - cls.startTime

        title = "포인트 봇 정보"
        text = f"포인트 봇 정보\n" \
               f"실행 시간: {cls.startTime}\n" \
               f"동작 시간: {runningTime.days}일, {runningTime.seconds}초\n" \
               f"잠수 리스트: {sleepList}\n"

        em = Embed(title=title, description=text)
        return em
