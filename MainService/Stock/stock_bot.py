import asyncio
from logging import getLogger

from discord.embeds import Embed
from discord.ext import commands

from MainService.Stock.stock_engine import StockEngine

log = getLogger(__name__)


class StockBot(commands.Cog):
    """
    주식 봇
    모의 주식을 담당하는 봇이다.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def stock(self, ctx):
        """
        주식 명령어
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('해당 명령어가 없습니다.\n 명령어를 제대로 입력해 주세요')

    @stock.command()
    async def buy(self, ctx, code, quantity):
        """
        주식 구입
        """
        name = ctx.author.name
        try:
            quantity = int(quantity)
            embed = StockEngine.buy(name, code, quantity)
        except ValueError:
            title = "주식 매수 실패"
            text = f"수량을 잘못 입력하셨습니다.\n" \
                   f"입력값: {quantity} "
            embed = Embed(title=title, description=text)

        except Exception as e:
            title = "주식 매수 실패 - 예상치 못한 오류로 매수에 실패하였습니다."
            text = f"발생 오류: {e}"
            embed = Embed(title=title, description=text)

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @stock.command()
    async def sell(self, ctx, code, quantity):
        """
        주식 판매
        """
        name = ctx.author.name
        quantity = int(quantity)
        embed = StockEngine.sell(name, code, quantity)
        try:
            print("hello")

        except ValueError:
            title = "주식 매매 실패"
            text = f"수량을 잘못 입력하셨습니다.\n" \
                   f"입력값: {quantity} "
            embed = Embed(title=title, description=text)

        except Exception as e:
            title = "주식 매수 실패 - 예상치 못한 오류로 매수에 실패하였습니다."
            text = f"발생 오류: {e}"
            embed = Embed(title=title, description=text)

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @stock.command()
    async def info(self, ctx):
        """
        주식 조회
        현재 내가 소유한 주식을 보여준다.
        """
        name = ctx.author.name
        embed = StockEngine.info(name)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @stock.command()
    async def search(self, ctx, code):
        """
        주식 검색
        """
        embed = StockEngine.search(code)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @stock.command()
    async def popular(self, ctx):
        """
        인기 있는 주식 리스트
        인기 있는 주식 리스트를 보여준다.
        업데이트시 매번 초기화 된다.
        """
        embed = StockEngine.popular()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제