from asyncio import Queue, QueueEmpty, create_task

class _AIterator:

    def __aiter__(self):
        return self

    async def __anext__(self):
        try: return await self.next()
        except QueueEmpty: raise StopIteration

class LeagueWarIterator(_AIterator):
    __slots__ = ('__iteration', '__war_tags', '__kwargs', 'client', '__filled')

    def __init__(self, war_tags, client, **kwargs):
        self.__iteration = Queue()
        self.__war_tags = war_tags
        self.__kwargs = kwargs
        
        self.client = client
        self.__filled = False

    async def _calculate(self, tag):
        return await self.client.fetch_round_war(tag)

    async def _fill(self):
        # self.__filled = True
        for tag in self.__war_tags:
            task = create_task(self._calculate(tag))
            await self.__iteration.put(task)

    async def next(self):
        if self.__iteration.empty():
            await self._fill()

        return await self.__iteration.get_nowait()