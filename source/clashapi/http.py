import asyncio

from collections import deque
from itertools import cycle
from time import process_time

import aiohttp

from .utils import LRUCache
from .errors import HTTPException

"""
header : {'authorization': "Bearer <API Token>"}
"""

class Throttler:

    def __init__(self, limit=10, per=1, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self.times = deque(maxlen=limit)

        self.per = per

    def __delete_element(self):
        self.times.popleft()

    async def __aenter__(self):
        # Waits for the queue to have an open slot
        while len(self.times) >= self.times.maxlen:
            print("Request throttled")
            await asyncio.sleep(0.001)

        # Appends the time to the process queue and assigns a coroutine to delete the element later
        self.times.append(process_time())
        self.loop.call_later(self.per, self.__delete_element)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_t):
        pass


class RequestInfo:
    BASE_URL = 'https://api.clashofclans.com/v1'

    def __init__(self, method, path, **kwargs):
        self.method = method,
        self.url = f'{self.BASE_URL}{path.replace("#", "%23")}'
        self.kwargs = kwargs

    def get(self, key, default=None):
        try: return self.kwargs[key]
        except KeyError: 
            self.kwargs.update({key: default})
            return default

    def cache_key(self):
        return self.url

class HTTPClient:
    """Client responsible for building the bridge between the Clash API and the python wrapper"""

    def __init__(self, tokens, throttle_limit=10, loop=None):
        self.tokens = cycle(tokens)
        self.loop = loop or asyncio.get_event_loop()
        
        self.__throttler = Throttler(limit=len(tokens)*throttle_limit)
        self.__cache = LRUCache(10000)
        self.__session = aiohttp.ClientSession()

    async def close(self):
        if self.__session:
            await self.__session.close()

    def _delete_cache_element(self, key):
        try: del self.__cache[key]
        except KeyError: pass

    async def request(self, info):
        current_token = next(self.tokens)
        headers = info.get('headers', {})
        headers.update({'Authorization': 'Bearer %s' % current_token})
        cache_key = info.cache_key()
        
        # Index cache for data
        if self.__cache is not None:
            try : 
                print("cache use attempted: {}".format(cache_key))
                return self.__cache[cache_key]
            except KeyError: print("cache use failed: {}".format(cache_key))

        
        async with self.__throttler.lock, self.__throttler:
            try:
                async with self.__session.request("get", info.url, **info.kwargs) as response:
                    data = await response.json()

                    try:
                        delete_after = int(response.headers['Cache-Control'].strip("max-age="))

                        if self.__cache is not None:
                            self.__cache[cache_key] = data
                            self.loop.call_later(delete_after, self._delete_cache_element, cache_key)
                    except (KeyError, AttributeError, ValueError): pass
                    
                    # Do things depending on status
                    if 200 <= response.status < 300: return data
                    else: raise HTTPException(response.status, "", data)
            except asyncio.TimeoutError:
                pass # Raise failed error or something

    async def fetch_clan(self, tag, **kwargs):
        return await self.request(RequestInfo('GET', f'/clans/{tag}', **kwargs))

    async def fetch_current_war(self, tag, **kwargs):
        return await self.request(RequestInfo('GET', f'/clans/{tag}/currentwar', **kwargs))

    async def fetch_clan_wars(self, tag, **kwargs):
        # Data returned by this should be similar to a list of currentWar, however some base values are different
        return await self.request(RequestInfo('GET', f'/clans/{tag}/warlog', **kwargs))

    async def fetch_clan_members(self, tag, **kwargs):
        # Data returned by this should be similar to a list of ClanMember
        return await self.request(RequestInfo('GET', f'/clans/{tag}/members', **kwargs))

    async def search_for_clans(self, search_info, **kwargs):
        # Data returned by this should be a list of Clans
        kwargs.update({'json': search_info})
        return await self.request(RequestInfo('GET', f'/clans', **kwargs))

    # Request User

    async def fetch_user(self, tag, **kwargs):
        return await self.request(RequestInfo('GET', f'/players/{tag}', **kwargs))
