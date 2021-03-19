"""
main
1. 로그를 생성
2. 봇을 생성하고 실행
"""
import json
from logging import getLogger
from logging.config import dictConfig

from DiscordBot4.MainBot import MyBot
from settings import discord_token

if __name__ == '__main__':
    # 로그 생성
    with open('logs/loggers.json') as f:
        config = json.load(f)
        dictConfig(config)

    log = getLogger(__name__)

    log.info('start programe')
    client = MyBot()


    @client.event
    async def on_ready():
        log.info('Logged in as {0} ({0.id})'.format(client.user))

    client.run(discord_token)
