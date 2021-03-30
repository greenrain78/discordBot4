import asyncio
from discord.ext import commands

from Chat.chat_engine import ChatEngine
from Log.infoLog import logger as log


class ChatBot(commands.Cog):
    def __init__(self, para_bot):
        self.bot = para_bot
        self.engine = ChatEngine()

    @commands.command()
    async def userblock(self, ctx, user, time):
        """
        해당 유저 조용히 시키기
        """
        try:
            name = ctx.message.author.name
            if name == '김대원':
                text = self.engine.userBlock(user, time)

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
        except Exception as e:
            log.exception("command botState error")

    @commands.command()
    async def clearblock(self, ctx):
        """
        해당 유저 조용히 시키기
        """
        try:
            name = ctx.message.author.name
            if name == '김대원':
                self.engine.clearList()
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
        except Exception as e:
            log.exception("command botState error")

    async def checkBlock(self, message):
        try:
            name = message.author.name
            if self.engine.checkUser(name):
                await message.delete()
                text = self.engine.getUser(name)
                msg = await message.channel.send(text)
                await asyncio.sleep(1)
                await msg.delete()  # 메세지 삭제

        except Exception as e:
            log.exception("command botState error")
