import asyncio
from logging import getLogger

from discord.ext import commands

from SubService.Basic.basic_engine import BasicEngine

log = getLogger(__name__)


class BasicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def state(self, ctx):
        """
        디코 봇 상태 확인
        """
        embed = BasicEngine.get_state()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @commands.command()
    async def github(self, ctx):
        """
        디코 봇 깃허브 링크
        """
        text = 'https://github.com/greenrain78/discordBot4'
        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @commands.command()
    async def report(self, ctx):
        """
        정식적으로 디코봇 버그 리포트 제출
        """
        embed = BasicEngine.report_issue()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제
