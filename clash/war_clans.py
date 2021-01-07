import typing

from clash.abc import BaseClan, MemberContainer
from clash.utils import build_list

from .war_members import WarMember, LeagueMember

class WarClan(BaseClan, MemberContainer):
    """Represents a clan in a War
    """
    
    __slots__ = (
        'war',

        'attacks_used',
        'stars_gained',
        'destruction_caused',
        '__member_dict',

        'is_cwl'
    )

    def __init__(self, data, client, war, is_cwl=False):
        super().__init__(data, client)
        
        # War is currently unbuilt and probably shouldn't be used other than a reference
        self.war = war

        self.attacks_used:int = data.get('attacks', 0)
        self.stars_gained:int = data.get('stars', 0)
        self.destruction_caused:float = data.get('destructionPercentage', 0)
        
        self.__member_dict = dict({
            mdata.get('tag'): WarMember(mdata, client=client) for mdata in data.pop('members', [])
        })

        self.is_cwl = is_cwl

    @property
    def members(self) -> typing.List[WarMember]:
        return list(self.__member_dict.values())
    
    @property
    def attacks_left(self):
        return (self.war.team_size * (1 if self.is_cwl else 2)) - self.attacks_used

    # def get_member(self, tag):
    #     pass


class LeagueClan(BaseClan, MemberContainer):
    """Represents a clan in a LeagueGroup"""
    
    __slots__ = ('__member_dict')

    def __init__(self, data, client):
        self.__member_dict = dict({
            mdata.get('tag'): LeagueMember(mdata, league_group=self) for mdata in data.pop('members', [])
        })

        super().__init__(data, client)

    @property
    def members(self):
        return list(self.__member_dict.values())