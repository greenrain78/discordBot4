import asyncio
from logging import getLogger

from discord.ext import commands

from SubService.Basic.basic_engine import BasicEngine

log = getLogger(__name__)


class BasicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def basic(self, ctx):
        """
        basic 명령어
        디코 봇에 대한 기본 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help basic"
            await ctx.send(text)

    @basic.command()
    async def state(self, ctx):
        """
        디코 봇 상태 확인
        """
        name = ctx.message.author.name

        embed = BasicEngine.get_state()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제


    @basic.command()
    async def github(self, ctx):
        """
        디코 봇 깃허브 링크
        """
        text = 'https://github.com/greenrain78/discordBot4'
        msg = await ctx.send(text)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

