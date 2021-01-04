import datetime
from typing import Tuple

from clash.abc import BaseClan, ClashObject
from clash.enums import WarState
from clash.utils import build_list, format_time, execute_if_found

from .war_clans import WarClan, LeagueClan

# Defines a war in Clash
class War(ClashObject):
    """Represents a clan war in Clash of Clans"""

    __slots__ = (
        'state',

        'team_size',
        'preparation_start',
        'battle_start',
        'battle_end',
        'team_one',
        'team_two',

        'is_cwl',       

        'client'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} team_one={0.team_one} team_two={0.team_two}>'.format(self)

    def __init__(self, data, client, is_cwl=False):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self.state = WarState.from_data(data.get('state')) # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self.team_size = data.get('teamSize', 0),
        self.preparation_start = execute_if_found(data, 'preparationStartTime', format_time, default=datetime.datetime.min)
        self.battle_start = execute_if_found(data, 'startTime', format_time, default=datetime.datetime.min)
        self.battle_end = execute_if_found(data, 'endTime', format_time, default=datetime.datetime.min)

        self.is_cwl = is_cwl

        self.client = client

        # Team order will always be the same, no matter what clan was requested
        self.team_one = WarClan(data.get('clan'), client, self)
        self.team_two = WarClan(data.get('opponent'), client, self)

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
    
    __slots__ = ('__war_tags')

    def __init__(self, data, clans):
        self.__war_tags = data.pop('warTags')


class LeagueGroup(ClashObject):
    """Represents a Clan War League Group in Clash of Clans
    """

    __slots__ = ('state', 'season', '__raw_rounds', '__clan_dict', 'client')

    def __init__(self, data, client):
        self.state = data.pop('state') # Unsure what this can be other than (preparation, inWar) # Should also be an enum
        self.season = data.pop('season') # In format of YEAR-MONTH EX. 2021-01
        self.__clan_dict = dict({
            lcdata.get('name'): LeagueClan(lcdata, client=client) for lcdata in data.pop('clans', [])
        })
        # a list of warTags with that reference a ClanWar (will it still reference clanwar after over? or clanwar result?)
        self.__raw_rounds = data.pop('rounds', [])

        self.client = client

    @property
    def clans(self):
        return list(self.__clan_dict.values())