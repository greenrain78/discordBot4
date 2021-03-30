import threading
from datetime import datetime
from logging import getLogger
from time import sleep
log = getLogger(__name__)


class ChatEngine:
    blockList = {}

    def __init__(self):
        log.info("BasicEngine init 실제 동작 안함")

    @classmethod
    def userBlock(cls, name: str, time: int) -> str:
        # 미존재시
        if name not in cls.blockList:
            cls.blockList[name] = (time, datetime.now())
            th = threading.Thread(target=cls.userSleep, args=(name, time))
            th.start()

            text = f"유저[{name}]을 {time}동안 성공적으로 침묵시켰습니다."
        else:
            text = cls.getUser(name)
        return text

    @classmethod
    def getUser(cls, name) -> str:
        user = cls.blockList.get(name)
        text = f"유저[{name}]을 {user[1]}부터 {user[0]}동안 침묵중"
        return text

    @classmethod
    def userSleep(cls, name, time):
        sleep(int(time))
        del cls.blockList[name]

    @classmethod
    def checkUser(cls, name) -> bool:
        if name in cls.blockList:
            return True
        else:
            return False

    @classmethod
    def clearList(cls):
        cls.blockList.clear()
