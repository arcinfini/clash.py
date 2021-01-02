import typing

from .http import HTTPClient

from clash.abc import BaseUser, BaseClan
from .clans import Clan
from .users import User
from .war import War, LeagueGroup

class ClashClient:
    
    def __init__(self, tokens:typing.List):
        self.__httpclient = HTTPClient(tokens)
    
    async def close(self):
        await self.__httpclient.close()

    async def fetch_clan(self, tag:str, cls=Clan):
        if not issubclass(cls, BaseClan):
            raise TypeError('cls is not a subclass of BaseClan')

        data = await self.__httpclient.fetch_clan(tag)
        clan = cls(data, client=self)
        return clan

    async def fetch_current_war(self, tag:str, cls=War) -> War:
        if not issubclass(cls, War):
            raise TypeError('cls is not a subclass of War')
        
        # Account for private war logs
        data = await self.__httpclient.fetch_current_war(tag)
        war = War(data, client=self)
        return war
        
    # User Fetches

    async def fetch_user(self, tag:str, cls=User):
        if not issubclass(cls, BaseUser):
            raise TypeError('cls is not a subclass of BaseUser')
        
        data = await self.__httpclient.fetch_user(tag)
        user = cls(data, client=self)
        return user

    # Clan War League Fetches

    async def fetch_league_group(self, tag) -> LeagueGroup:
        data = await self.__httpclient.fetch_league_group(tag)
        league_group = LeagueGroup(data, client=self)
        return league_group