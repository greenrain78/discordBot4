import asyncio
from logging import getLogger
from discord.ext import commands

from MainService.Point.point_engine import PointEngine
from settings import robot_user

log = getLogger(__name__)


class PointBot(commands.Cog):
    """
    포인트 봇
    디스코드 포인트 조회및 출석채크 기능을 담당하는 봇이다.
    """
    def __init__(self, bot):
        self.bot = bot
        self.engine = PointEngine()

    @commands.group()
    async def point(self, ctx):
        """
        디코 포인트 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help point"
            await ctx.send(text)

    @point.command()
    async def mine(self, ctx):
        """
        내 포인트 조회
        현재 내 포인트를 보여준다.
        """
        user = ctx.author.name
        text = self.engine.getPoint(user)
        # msg = await ctx.send(embed=embed)
        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @point.command()
    async def event(self, ctx):
        """
        내 포인트 조회
        현재 내 포인트를 보여준다.
        """
        embed = self.engine.eventInfo()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    async def dailyCheck(self, message):
        name = message.author.name
        if name in robot_user:
            return None

        text = self.engine.dailyCheck(name)
        if text is None:    # 중복 채팅 무시
            return None

        msg = await message.channel.send(text)
        await asyncio.sleep(10)
        await msg.delete()  # 메세지 삭제
