import enum
from typing import List, Optional, Dict

import requests


class ErbsClient(object):
    """
    블서 api
    """
    BASE_URL = 'https://open-api.bser.io'
    api_key: Optional[str] = None
    version: Optional[str] = None

    def __init__(self, api_key: str, version: str = 'v1'):
        self.api_key = api_key
        self.version = version

    class MatchingTeamMode(enum.Enum):
        SOLO = 1
        DUO = 2
        SQUAD = 3

    @property
    def api_url(self) -> str:
        return f'{self.BASE_URL}/{self.version}'

    @property
    def header_data(self) -> dict:
        return {
            'Accept': 'application/json',
            'X-Api-Key': self.api_key,
        }

    async def fetch_user_nickname(self, name: str) -> int:
        url = f'{self.api_url}/user/nickname?query={name}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        # get userNum
        userInfo = json_resp.get("user", [])
        return userInfo['userNum']

    async def fetch_user_games(self, user_number: int) -> List[dict]:
        url = f'{self.api_url}/user/games/{user_number}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get("userGames", [])

    async def fetch_user_stats(self,
                               user_number: Optional[int],
                               season_id: int = 1) -> Dict:
        if not user_number:
            raise ValueError('user_number 인자가 없습니다')

        url = f'{self.api_url}/user/stats/{user_number}/{season_id}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get("userStats", [])

    async def fetch_meta_data(self, meta_type: str = 'hash') -> List[dict]:
        url = f'{self.api_url}/data/{meta_type}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get("data", [])

    async def fetch_rank_top(self, season_id: int = 1, matching_team_mode: int = 1) -> List[dict]:
        url = f'{self.api_url}/rank/top/{season_id}/{matching_team_mode}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get("topRanks", [])

    async def fetch_rank_user(self,
                              user_number: Optional[int],
                              season_id: int = 1,
                              matching_team_mode: int = 1) -> Dict:
        if not user_number:
            raise ValueError('user_number 인자가 없습니다')

        url = f'{self.api_url}/rank/{user_number}/{season_id}/{matching_team_mode}'
        response = requests.get(url, headers=self.header_data)
        json_resp = response.json()
        if response.status_code != 200:
            raise ValueError(json_resp.get('message', 'API Error'))

        return json_resp.get("userRank", {})
