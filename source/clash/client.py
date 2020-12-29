import typing

from .http import HTTPClient

from .clans import Clan
from .users import User
from .war import War

class ClashClient:
    
    def __init__(self, tokens:typing.List):
        self.__httpclient = HTTPClient(tokens)
    
    async def close(self):
        await self.__httpclient.close()

    async def fetch_clan(self, tag):
        data = await self.__httpclient.fetch_clan(tag)
        clan = Clan(data)
        return clan

    async def fetch_current_war(self, tag) -> War:
        data = await self.__httpclient.fetch_current_war(tag)
        war = War(data)
        return war
        