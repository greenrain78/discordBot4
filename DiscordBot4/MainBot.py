from logging import getLogger

from discord.ext import commands

from MainService.ERBS.erbs_bot import ERBSBot
from settings import debug, test_server_id

log = getLogger(__name__)


class MyBot(commands.Bot):

    def __init__(self):
        prefix = commands.when_mentioned_or("$")
        desc = 'GreenRain discord bot 4.0.2'
        super(MyBot, self).__init__(command_prefix=prefix, description=desc)

        # # create bot
        # self.pointBot = PointBot(self)
        self.erbsBot = ERBSBot(self)
        # self.basicBot = BasicBot(self, pointBot=self.pointBot, erbsBot=self.erbsBot)
        # self.gameBot = GameBot(self)
        # self.chatBot = ChatBot(self)
        # self.stockBot = StockBot(self)
        #
        # # add bot
        # self.add_cog(self.pointBot)
        self.add_cog(self.erbsBot)
        # self.add_cog(self.basicBot)
        # self.add_cog(self.gameBot)
        # self.add_cog(self.chatBot)
        # self.add_cog(self.stockBot)

    async def on_message(self, message):
        log.info('{0.author}: {0.content} - {0.guild} ({0.channel})'.format(message))
        if debug:
            if message.guild != self.get_guild(test_server_id):
                log.info('디버깅중 디버깅 서버가 아닙니다.')
                return None
        else:
            if message.guild == self.get_guild(test_server_id):
                log.info('배포중 디버깅 서버에서는 동작하지 않습니다.')
                return None

        # await self.chatBot.checkBlock(message)
        await super(MyBot, self).on_message(message)
        # await self.pointBot.dailyCheck(message)
