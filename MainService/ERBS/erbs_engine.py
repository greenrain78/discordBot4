from logging import getLogger

import discord

from MainService.ERBS.ERBS_api_client import ErbsClient
from settings import erbs_api_key

api_key = erbs_api_key
version = 'v1'

log = getLogger(__name__)


class ErbsEngine:
    # API Client 생성
    erbsAPI = ErbsClient(api_key=api_key, version=version)

    @classmethod
    async def recent(cls, name: str):
        # 경기 데이터 수집
        log.debug('user name: %s', name)
        user_num = await cls.erbsAPI.fetch_user_nickname(name)
        log.debug('user_num: %s', user_num)
        result = await cls.erbsAPI.fetch_user_games(user_num)
        log.debug('result = \n  %s', result)
        game = result[0]  # 제일 마지막 판

        # 메세지 제작
        title = f"{name}의 최근 경기 기록"
        text = f"등수: {game['gameRank']}\n" \
               f"플래이어 킬: {game['playerKill']}\n" \
               f"어시스트: {game['playerAssistant']}\n" \
               f"동물 킬: {game['monsterKill']}\n" \
               f"{game['killDetail']}({game['killer']})에게 {game['causeOfDeath']}으로 죽었습니다.\n"
        em = discord.Embed(title=title, description=text)

        title1 = "피해량"
        text1 = f"플레이어에게 준 피해: {game['damageToPlayer']}\n" \
                f"플레이어에게 받은 피해: {game['damageFromPlayer']}\n" \
                f"동물에게 준 피해: {game['damageToMonster']}\n" \
                f"동물에게 받은 피해: {game['damageFromMonster']}\n"

        em.add_field(name=title1, value=text1, inline=False)

        title2 = "숙련도"
        text2 = f"캐릭터 레벨: {game['characterLevel']}\n" \
                f"사용 무기: {game['bestWeapon']}\n" \
                f"무기 숙련도: {game['bestWeaponLevel']}\n"
        em.add_field(name=title2, value=text2, inline=False)

        title3 = "플래이 타임"
        text3 = f"플래이 시작 시간: {game['startDtm']}\n" \
                f"플래이 타임: {int(game['duration'] / 60)}분 {game['duration'] % 60}초\n" \
                f"남은 금지 구역: {game['safeAreas']}\n"
        em.add_field(name=title3, value=text3, inline=False)

        footer = f"유저 코드: {game['userNum']}, 이전 mmr: {game['mmrBefore']}"
        em.set_footer(text=footer)
        return em

    @classmethod
    async def recent_list(cls, name: str):
        # 경기 데이터 수집
        log.debug('user name: %s', name)
        user_num = await cls.erbsAPI.fetch_user_nickname(name)
        log.debug('user_num: %s', user_num)
        result = await cls.erbsAPI.fetch_user_games(user_num)
        log.debug('result = \n  %s', result)

        # 메세지 제작
        title = f"{name}의 최근 경기 리스트"
        text = ""

        for game in result:
            text += f"등수: {game['gameRank']}\n" \
                    f"플래이어 킬: {game['playerKill']}\n" \
                    f"어시스트: {game['playerAssistant']}\n" \
                    f"동물 킬: {game['monsterKill']}\n" \
                    f"{game['killDetail']}({game['killer']})에게 {game['causeOfDeath']}으로 죽었습니다.\n\n"

        em = discord.Embed(title=title, description=text, inline=False)

        return em

    @classmethod
    async def user_info(cls, name: str):
        # 경기 데이터 수집
        log.debug('user name: %s', name)
        user_num = await cls.erbsAPI.fetch_user_nickname(name)
        log.debug('user_num: %s', user_num)
        result = await cls.erbsAPI.fetch_user_stats(user_num)
        log.debug('result = \n  %s', result)
        # 메세지 제작
        title = f"{name}의 최근 경기 리스트 - 시즌: {result[0]['seasonId']}"
        text = "----------솔로-----------------------듀오-----------------------스쿼드-----------"
        em = discord.Embed(title=title, description=text, inline=False)

        print("-------------------------")
        for game in result:
            print(game)
            title1 = f"matchingTeamMode: {game['matchingTeamMode']}"
            text1 = f"mmr: {game['mmr']}\n" \
                    f"랭크: {game['rank']}\n" \
                    f"rankSize: {game['rankSize']}\n" \
                    f"상위: {game['rankPercent']*100}%\n" \
                    f"게임수: {game['totalGames']}\n" \
                    f"총 승리수: {game['totalWins']}\n" \
                    f"평균 Rank: {game['averageRank']}\n" \
                    f"평균 Kills: {game['averageKills']}\n" \
                    f"평균 Assistants: {game['averageAssistants']}\n" \
                    f"평균 Hunts: {game['averageHunts']}\n" \
                    f"top1: {game['top1']}\n" \
                    f"top2: {game['top2']}\n" \
                    f"top3: {game['top3']}\n" \
                    f"top5: {game['top5']}\n" \
                    f"top7: {game['top7']}\n"
            em.add_field(name=title1, value=text1, inline=True)

        footer = f"유저 코드: {result[0]['userNum']}"
        em.set_footer(text=footer)

        return em


    @classmethod
    async def mmr_list(cls, name: str):
        # To do 미구형
        # 경기 데이터 수집
        # log.debug('user name: %s', name)
        # user_num = await cls.erbsAPI.fetch_user_nickname(name)
        # log.debug('user_num: %s', user_num)
        # stats_result = await cls.erbsAPI.fetch_user_stats(user_num)
        # log.debug('fetch_user_stats result = \n  %s', stats_result)
        # await asyncio.sleep(60)
        # games_result = await cls.erbsAPI.fetch_user_games(user_num)
        # log.debug('fetch_user_games result = \n  %s', games_result)
        #
        # # 메세지 제작
        # title = f"{name}의 최근 경기 리스트"
        # text = f"솔로{name}"
        #
        # for game in games_result:
        #     text += f"등수: {game['gameRank']}\n" \
        #        f"플래이어d 킬: {game['playerKill']}\n" \
        #        f"어시스트: {game['playerAssistant']}\n" \
        #        f"동물 킬: {game['monsterKill']}\n" \
        #        f"{game['killDetail']}({game['killer']})에게 {game['causeOfDeath']}으로 죽었습니다.\n\n"
        #
        # em = discord.Embed(title=title, description=text, inline=False)

        # return em
        pass


