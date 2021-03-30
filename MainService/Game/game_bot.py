import asyncio
from logging import getLogger

from discord.ext import commands

from MainService.Game.bet_engine import BetEngine
from MainService.Game.game_engine import Gameboard
from MainService.Point.point_DB import PointDB
log = getLogger(__name__)


class GameBot(commands.Cog):
    max_point = 10000

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def game(self, ctx):
        """
        디코 게임 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help game"
            await ctx.send(text)

    @classmethod
    def checkPoint(cls, user, pt) -> str:
        mypoint = PointDB.get_point(user)
        if pt < 0 or mypoint < pt:
            text = f"{user}님 보유 포인트가 부족합니다.\n" \
                   f"입력하신 포인트: {pt}, 보유 포인트: {mypoint}"
        elif cls.max_point < pt:
            text = f"입력하신 포인트가 도박의 마지노선을 넘었습니다.\n" \
                   f"저희가 감당할 수 있는 액수가 아니예요. 저희 돈이 없어요 ㅠㅠ\n" \
                   f"입력하신 포인트: {pt}, 마지노선: {cls.max_point}"
        else:
            text = ""
        return text

    @game.command()
    async def even(self, ctx, point, *args):
        """
        홀짝 게임
        0~99사이의 랜덤한 숫자가 생기는데 해당 숫자가 홀인지 짝인지 맞추는 게임
        """
        user = ctx.author.name
        try:
            pt = int(point)
            check = self.checkPoint(user=user, pt=pt)
            if check:
                text = check
            else:
                text = Gameboard.odd_even(user, pt, args)
        except ValueError:
            text = f'{point}는 숫자가 아닙니다.'

        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @game.command()
    async def coin(self, ctx, point, game_name, *args):
        """
        동전 게임
        동전을 던지는데 동전이 앞면인지 뒷면인지 맞추는 게임
        """
        user = ctx.author.name
        try:
            pt = int(point)
            check = self.checkPoint(user=user, pt=pt)
            if check:
                text = check
            else:
                text = Gameboard.coin(user, pt, args)
        except ValueError:
            text = f'{point}는 숫자가 아닙니다.'

        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @commands.group()
    async def bet(self, ctx):
        """
        배팅 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help game"
            await ctx.send(text)

    @bet.command()
    async def open(self, ctx, *context):
        """
        포인트 배팅을 연다
        """
        name = ctx.author.name
        text = BetEngine.openBet(name, context)
        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @bet.command()
    async def close(self, ctx, result):
        """
        포인트 배팅을 닫는다.
        """
        name = ctx.author.name
        if result == "승":
            text = BetEngine.closeBet(name, True)
        elif result == "패":
            text = BetEngine.closeBet(name, False)
        else:
            text = f"예측 결과를 잘못 입력하셨습니다.\n" \
                   f"{result}: 승 또는 패 라고 입력해 주시기 바랍니다. ^^\n"

        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @bet.command()
    async def info(self, ctx):
        """
        현재 열려있는 포인트 배팅을 보여준다.
        """
        name = ctx.author.name
        em = BetEngine.infoBet(name)

        msg = await ctx.send(embed=em)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @bet.command()
    async def betting(self, ctx, point, arg):
        """
        포인트 배팅!!!!!!!!!!!!
        """
        user = ctx.author.name
        pt = int(point)
        check = self.checkPoint(user=user, pt=pt)
        if check:
            text = check
        elif arg == "승":
            text = f"승리에 참여하셨습니다\n"
            text += BetEngine.betting(user, pt, True)
        elif arg == "패":
            text = f"패배에 참여하셨습니다\n"
            text += BetEngine.betting(user, pt, False)
        else:
            text = f"예측 결과를 잘못 입력하셨습니다.\n" \
                   f"{arg}: 승 또는 패 라고 입력해 주시기 바랍니다. ^^\n"

        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

