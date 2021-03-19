import discord
from discord.embeds import Embed

from MainService.Point.point_DB import PointDB
from settings import superuser


class BetEngine:
    open_user = ""
    win = 1
    loss = 1
    context = ""
    userList = {}

    @classmethod
    def openBet(cls, name: str, context) -> str:
        if cls.open_user:
            return f"이미 {cls.open_user}가 배팅을 열었습니다."

        cls.open_user = name
        cls.context = context
        text = f"{cls.open_user}가 배팅을 열었습니다\n" \
               f"{cls.context}\n" \
               f"많은 참여 바랍니다."
        return text

    @classmethod
    def closeBet(cls, name: str, result: bool) -> str:
        text = ""
        if not cls.open_user:
            return f"현재 배팅이 열려있지 않습니다.\n"

        text += f"배팅을 종료합니다.\n"
        if name == cls.open_user or name == superuser:
            text += f"정상 종료하였습니다.\n"
        else:
            text += f"배팅이 여신 사용자가 아니므로 배팅 종료를 취소합니다.\n"
            return text

        text += f"예측 결과는 {'승리' if result else '패배'}\n" \
                f"총 {cls.win + cls.loss}포인트를 획득하셨습니다.\n"

        # 정산
        for user, values in cls.userList.items():
            if values[0] == result:
                point = (cls.win+cls.loss)/(cls.win if result else cls.loss) * values[1]
                cls.update_point(user, point,
                                 reason=f"{cls.open_user}가 주최한 도박에서 {result}로 {point}만큼 배팅에 성공하셨습니다.")
                text += f"{user}가 {point}를 획득하셨습니다.\n"
        # 지우기
        cls.open_user = ""
        cls.win = 1
        cls.loss = 1
        cls.context = ""
        cls.userList.clear()

        return text

    @classmethod
    def betting(cls, name: str, point: int, predic: bool) -> str:
        if name in cls.userList and cls.userList[name][0] != predic:
            text = f"승리 패배에 동시에 배팅할 수 없습니다.\n"
            return text

        text = f"배팅으로 입력하신 {point} 포인트 만큼 차감됩니다.\n"
        cls.update_point(name, -point,
                         reason=f"{cls.open_user}가 주최한 도박에서 {predic}로 {point}만큼 배팅하셨습니다.")

        # 유저 리스트에 추가
        if name in cls.userList:
            cls.userList[name][1] += point
        else:
            cls.userList[name] = [predic, point]
        text += f"총 {cls.userList[name][1]}만큼 배팅하셨습니다.\n"
        # 등록
        if predic:
            cls.win += point
        else:
            cls.loss += point
        return text

    @classmethod
    def infoBet(cls, name) -> Embed:
        if not cls.open_user:
            title = "디스코드 실시간 예측!"
            text = f"주최: {'아무도 없어요 ㅠㅠ'}, 주관: 대원컴퍼니, testbot"
            em = discord.Embed(title=title, description=text)
        else:
            # 배율 계산

            # 내용
            title = "디스코드 실시간 예측!"
            text = f"주최: {cls.open_user}, 주관: 대원컴퍼니, testbot"
            em = discord.Embed(title=title, description=text)

            title1 = "내용"
            text1 = cls.context
            em.add_field(name=title1, value=text1, inline=False)

            title2 = "현황"
            text2 = f"총합 포인트: {cls.win + cls.loss}\n"
            text2 += f"승리\n" \
                     f"인원: {[user for user in cls.userList if cls.userList[user][0]]}\n" \
                     f"총 포인트: {cls.win}\n" \
                     f"배율: {(cls.win + cls.loss) / cls.win}\n"
            text2 += f"패배\n" \
                     f"인원: {[user for user in cls.userList if not cls.userList[user][0]]}\n" \
                     f"총 포인트: {cls.loss}\n" \
                     f"배율: {(cls.win + cls.loss) / cls.loss}\n"

            em.add_field(name=title2, value=text2, inline=False)
            title3 = "배팅 현황"
            if name in cls.userList:
                text3 = f"배팅: {'승리' if cls.userList[name][0] else '패배'}" \
                        f"배팅 포인트: {cls.userList[name][1]}"
            else:
                text3 = "쫄?"

            em.add_field(name=title3, value=text3, inline=False)

            footer = '가즈아!!!!!!!'
            em.set_footer(text=footer)
        return em

    @classmethod
    def update_point(cls, user: str, point: int, reason: str):
        PointDB.earn_point_user(user, point, reason)
        PointDB.update_game_count_user(user)
        text = f"획득 포인트: {point}"
        return text
