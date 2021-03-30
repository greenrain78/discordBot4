import asyncio
from logging import getLogger

from discord.ext import commands

from SubService.Chat.chat_engine import ChatEngine
from settings import superuser

log = getLogger(__name__)


class ChatBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def chat(self, ctx):
        """
        basic 명령어
        디코 봇에 대한 기본 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help basic"
            await ctx.send(text)

    @chat.command()
    async def block(self, ctx, user, time):
        """
        해당 유저 조용히 시키기
        """
        name = ctx.message.author.name
        if name == superuser:
            text = ChatEngine.userBlock(user, time)

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

    @chat.command()
    async def clear(self, ctx):
        """
        해당 유저 조용히 시키기
        """
        name = ctx.message.author.name
        if name == '김대원':
            ChatEngine.clearList()
            text = f"block list가 초기화 되었습니다."

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

    async def checkBlock(self, message):
        try:
            name = message.author.name
            if ChatEngine.checkUser(name):
                await message.delete()
                text = ChatEngine.getUser(name)
                msg = await message.channel.send(text)
                await asyncio.sleep(1)
                await msg.delete()  # 메세지 삭제

        except Exception as e:
            log.exception("command checkBlock error")
