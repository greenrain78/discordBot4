import asyncio
from logging import getLogger

from discord.ext import commands

from MainService.ERBS.erbs_engine import ErbsEngine

log = getLogger(__name__)


class ERBSBot(commands.Cog):
    """
    블서 봇
    블서에 대한 명령어를 담당하는 봇이다.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def bser(self, ctx):
        """
        블서 명령어
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('해당 명령어가 없습니다.\n 명령어를 제대로 입력해 주세요')

    @bser.command()
    async def recent(self, ctx, name: str):
        """
        블서 최근 전적 조회
        입력한 사용자의 가장 최근에 플래이한 블서 경기 내역을 보여준다.
        """
        embed = await ErbsEngine.recent(name)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제


    @bser.command()
    async def list(self, ctx, name: str):
        """
        블서 최근 전적 조회
        입력한 사용자의 가장 최근에 플래이한 블서 경기 내역을 보여준다.
        """
        embed = await ErbsEngine.recent_list(name)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @bser.command()
    async def mmr(self, ctx, name: str):
        """
        블서 mmr 변동 조회 - api 요청 부족으로 미구현
        사용자의 mmr 변동폭을 조회하여 보여준다.
        """
        #
        # embed = await ErbsEngine.mmr_list(name)
        # msg = await ctx.send(embed=embed)
        # await asyncio.sleep(60)
        #
        # await ctx.message.delete()  # 입력된 명령 제거
        # await msg.delete()  # 메세지 삭제

    @bser.command()
    async def user(self, ctx, name: str):
        """
        블서 유저 상태 정보 조회
        유저의 블서 통계 정보를 보여준다.
        """

        embed = await ErbsEngine.user_info(name)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

