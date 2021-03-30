import threading
from datetime import datetime
from time import sleep


class ChatEngine:
    blockList = {}

    def __init__(self):
        pass

    def userBlock(self, name: str, time: int) -> str:
        # 미존재시
        if name not in self.blockList:
            self.blockList[name] = (time, datetime.now())
            th = threading.Thread(target=self.userSleep, args=(name, time))
            th.start()

            text = f"유저[{name}]을 {time}동안 성공적으로 침묵시켰습니다."
        else:
            text = self.getUser(name)
        return text

    def getUser(self, name) -> str:
        user = self.blockList.get(name)
        text = f"유저[{name}]을 {user[1]}부터 {user[0]}동안 침묵중"
        return text

    def userSleep(self, name, time):
        sleep(int(time))
        del self.blockList[name]

    def checkUser(self, name) -> bool:
        if name in self.blockList:
            return True
        else:
            return False

    def clearList(self):
        self.blockList.clear()
