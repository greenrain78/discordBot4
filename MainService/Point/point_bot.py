import asyncio
from logging import getLogger
from discord.ext import commands

from MainService.Point.point_engine import PointEngine
from settings import robot_user, superuser

log = getLogger(__name__)


class PointBot(commands.Cog):
    """
    포인트 봇
    디스코드 포인트 조회및 출석채크 기능을 담당하는 봇이다.
    """

    def __init__(self, bot):
        self.bot = bot
        PointEngine.initSchedule()

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
        text = PointEngine.get_point(user)
        # msg = await ctx.send(embed=embed)
        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @point.command()
    async def give(self, ctx, user, point):
        """
        해당 사용자의 포인트를 갱신한다.
        주어진 포인트 만큼 사용자의 포인트를 감소하거나 증가시킨다.
        """
        name = ctx.message.author.name
        if name == superuser:
            pt = int(point)
            text = PointEngine.give_point(user, pt)

            msg = await ctx.send(text)
            await asyncio.sleep(60)

            await ctx.message.delete()  # 입력된 명령 제거
            await msg.delete()  # 메세지 삭제
        else:
            text = '허용되지 않은 사용자 입니다.'
            msg = await ctx.send(text)
            await asyncio.sleep(60)

            await ctx.message.delete()  # 입력된 명령 제거
            await msg.delete()  # 메세지 삭제

    @point.command()
    async def event(self, ctx):
        """
        디코 포인트 이벤트
        현재 진행중인 디코 이벤트를 알려준다.
        """
        embed = PointEngine.event_info()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    async def dailyCheck(self, message):
        name = message.author.name
        if name in robot_user:
            return None

        text = PointEngine.dailyCheck(name)
        if text is None:  # 중복 채팅 무시
            return None

        msg = await message.channel.send(text)
        await asyncio.sleep(10)
        await msg.delete()  # 메세지 삭제
