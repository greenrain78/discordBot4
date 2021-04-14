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
            await ctx.send(f'해당 명령어가 없습니다.\n'
                           f'명령어를 제대로 입력해 주세요\n'
                           f'$help stock')

    @commands.command()
    async def buy(self, ctx, company, quantity=None):
        """
        주식 구입
        """
        if quantity is None:
            title = "주식 매수 실패"
            text = f"매수할 수량을 입력해 주세요"
            embed = Embed(title=title, description=text)
        else:
            try:
                name = ctx.author.name
                quantity = int(quantity)
                embed = StockEngine.buy(name, company, quantity)
            except ValueError:
                title = "주식 매수 실패"
                text = f"수량을 잘못 입력하셨습니다.\n" \
                       f"입력값: {quantity} "
                embed = Embed(title=title, description=text)

        # except Exception as e:
        #     title = "주식 매수 실패 - 예상치 못한 오류로 매수에 실패하였습니다."
        #     text = f"발생 오류: {e}"
        #     embed = Embed(title=title, description=text)

        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @commands.command()
    async def sell(self, ctx, company, quantity):
        """
        주식 판매
        """
        try:
            name = ctx.author.name
            quantity = int(quantity)
            embed = StockEngine.sell(name, company, quantity)

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

    @commands.command()
    async def mystock(self, ctx):
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

    @commands.command()
    async def search(self, ctx, company, page_range=10):
        """
        주식 검색
        해당 주식을 검색한다.
        100영업일 만큼 해당하는 주식 정보를 가져와서 그래프로 보여준다.
        """
        async with ctx.typing():
            res = StockEngine.search(company, page_range)
        msg = await ctx.send(embed=res['embed'], file=res['image'])
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

    @stock.command()
    async def random(self, ctx, count=10):
        """
        주식 랜덤 리스트
        """
        embed = StockEngine.stock_ramdom_list(count)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제

    @commands.group()
    async def coin(self, ctx):
        """
        비트코인 명령어
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(f'해당 명령어가 없습니다.\n'
                           f'명령어를 제대로 입력해 주세요\n'
                           f'$help coin')

    @coin.command()
    async def list(self, ctx):
        """
        코인 리스트
        """
        async with ctx.typing():
            embed = StockEngine.coin_all_list()
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(60)

        await ctx.message.delete()  # 입력된 명령 제거
        await msg.delete()  # 메세지 삭제
