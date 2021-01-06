import datetime
import typing

from clash.abc import BaseClan, ClashObject, ClanContainer
from clash.enums import WarState
from clash.utils import build_list, format_time, execute_if_found, collect
from clash.iterators import LeagueWarIterator

from .war_clans import WarClan, LeagueClan

# Defines a war in Clash
class War(ClashObject, ClanContainer):
    """Represents a clan war in Clash of Clans"""

    __slots__ = (
        'state',

        'team_size',
        'preparation_start',
        'battle_start',
        'battle_end',
        '__clan_dict',

        'is_cwl',

        '_focused',
        # '__other',

        'client'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} team_one={0.team_one} team_two={0.team_two}>'.format(self)

    def __init__(self, data, client, is_cwl:bool=False, focused:str=None):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self.state = WarState.from_data(data.get('state')) # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self.team_size = data.pop('teamSize', 0)
        self.preparation_start = execute_if_found(data, 'preparationStartTime', format_time, default=datetime.datetime.min)
        self.battle_start = execute_if_found(data, 'startTime', format_time, default=datetime.datetime.min)
        self.battle_end = execute_if_found(data, 'endTime', format_time, default=datetime.datetime.min)

        self.is_cwl = is_cwl

        self.client = client

        # Team order will always be the same, no matter what clan was requested
        self.__clan_dict = {
            data.get('clan').get('tag') : WarClan(data.get('clan'), client, self, is_cwl=is_cwl), 
            data.get('opponent').get('tag'): WarClan(data.get('opponent'), client, self, is_cwl=is_cwl)
        }
        
        self._focused = self.__clan_dict.get(focused, None)

    @property
    def clans(self):
        """List[`WarClan`]: The clans that are a part of the war"""

        return list(self.__clan_dict.values())

    @property
    def team_one(self): 
        """`WarClan`: The first war clan in clans"""

        return self.clans[0]

    @property
    def team_two(self): 
        """`WarClan`: The second war clan in clans"""

        return self.clans[1]

    @property
    def focused(self):
        """`WarClan`: If focused is a passed kwarg to the class, 
        this will return the clan of the corresponding tag"""
        
        if self._focused is None: return None

        return self._focused

    def _set_focused(self, new:str):
        """Updates the value of the focused property
        
        Parameters
        ----------
        new : `str`
            The clan tag of the clan to set as focused

        Raises
        ------
        AttributeError: Raises an attribute error if the tag is not present in the war
        """
        
        try: 
            focused = self.__clan_dict[new]
            object.__setattr__(self, "_focused", focused) # Doesnt effectivly set the value??
        except KeyError:
            raise AttributeError(f'clan tag: {new} does not appear in this war')

    @property
    def other(self):
        """`WarClan`: If focused is a passed kwarg to the class, 
        this will return the clan of the other tag"""
        
        if self._focused is None: return None

        # Returns whatever is not selk.__focused
        return self.team_one if self.team_one is not self._focused else self.team_two

    @property
    def attacks(self):
        """Returns all the warattacks sorted by attack order"""
        pass

    @property
    def ahead(self):
        """Returns the clan that is currently winning"""
        pass


class LeagueRound(ClashObject):
    """Represents a round of wars in Clan War Leagues"""
    
    __slots__ = ('__war_tags', 'client')

    def __init__(self, data, client):
        self.__war_tags = data.pop('warTags')
        self.__wars = None
        self.client = client

    @property
    def wars(self) -> LeagueWarIterator:
        return LeagueWarIterator(self.__war_tags, self.client)

    @property
    def is_empty(self):
        return len(self.__war_tags) == 0 or self.__war_tags[0] == '#0'

    async def fetch_state(self):
        """Fetches the state of the round

        Returns
        -------
        The state of the round
        """
        war = await self.client.fetch_round_war(self.__war_tags[0])
        return war.state

    async def find_war(self, clan_tag) -> typing.Optional[War]:
        """Fetches the current war belonging to the clan tag

        Parameters
        ----------
        clan_tag : `str`
            The tag of the clan to search for

        Returns
        -------
        The focused war representation of the clan
        """

        iterator = LeagueWarIterator(self.__war_tags, self.client)
        async for war in iterator:
            # If the attempt to setting the focused clan is successful, it means that is the wanted war
            try: war._set_focused(clan_tag)
            except AttributeError: pass # Did not contain the clan we are looking for
            else: return war
        return None
            


class LeagueGroup(ClashObject, ClanContainer):
    """Represents a Clan War League Group in Clash of Clans
    """

    __slots__ = ('state', 'season', '__rounds', '__clan_dict', 'client')

    def __init__(self, data, client):
        self.state = data.pop('state') # Unsure what this can be other than (preparation, inWar) # Should also be an enum
        self.season = data.pop('season') # In format of YEAR-MONTH EX. 2021-01
        self.__clan_dict = dict({
            lcdata.get('name'): LeagueClan(lcdata, client=client) for lcdata in data.pop('clans', [])
        })
        
        self.__rounds = collect(
            (LeagueRound(rdata, client=client) for rdata in data.pop('rounds', [])),
            lambda r: not r.is_empty
        )

        self.client = client

    @property
    def clans(self) -> typing.List[LeagueClan]:
        """List[`LeagueClan`]: The clans that are part of the LeagueGroup"""
        return list(self.__clan_dict.values())

    async def fetch_war_round(self) -> typing.Optional[LeagueRound]:
        """Fetches the current war round

        Returns
        -------
        The round that is in the WarState of INWAR or the first preparation round: Optional[`LeagueRound`]
        """
        # Iterates a reversed list (order of most recent round to oldest) for the first InWar
        for round in reversed(self.__rounds):
            if await round.fetch_state() == WarState.INWAR:
                return round
        return self.__rounds[0]

    async def fetch_preparation_round(self) -> typing.Optional[LeagueRound]:
        """Fetches the current war preparation

        Returns
        -------
        The round that is in the WarState of PREPARATION: Optional[`LeagueRound`]
        """
        for round in reversed(self.__rounds):
            if await round.fetch_state() == WarState.PREPARATION:
                return round
        return None

    async def fetch_current_war(self, clan_tag) -> War:
        """Fetches the current War for the clan tag passed

        Parameters
        ----------
        clan_tag : `str`
            The tag of the clan to search for

        Returns
        -------
        The current war for the clan: `War`
        """
        current_round = await self.fetch_war_round()
        if current_round is None: return None
        result = await current_round.find_war(clan_tag)
        return result

    async def fetch_current_preparation(self, clan_tag) -> War:
        """Fetches the current preparation for the clan tag passed

        Parameters
        ----------
        clan_tag : `str`
            The tag of the clan to search for

        Returns
        -------
        The current preparation for the clan: `War`
        """

        preparation = await self.fetch_preparation_round()
        if preparation is None: return None
        result = await preparation.find_war(clan_tag)
        return result
