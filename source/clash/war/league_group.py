from clash.abc import ClashObject
from .league_clan import LeagueClan

class LeagueGroup(ClashObject):
    __slots__ = ('state', 'season', '__clan_dict', 'rounds')

    def __init__(self, data):
        self.state = data.pop('state') # Unsure what this can be other than (preparation, inWar) # Should also be an enum
        self.season = data.pop('season') # In format of YEAR-MONTH EX. 2021-01
        self.__clan_dict = dict({
            lcdata.get('name'): LeagueClan(lcdata) for lcdata in data.pop('clans', [])
        })
        self.rounds = () # a list of warTags with that reference a ClanWar (will it still reference clanwar after over? or clanwar result?)

    @property
    def clans(self):
        return self.__clan_dict.values()