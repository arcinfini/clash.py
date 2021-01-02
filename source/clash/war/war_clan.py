
from clash.abc import BaseClan, MemberContainer
from clash.utils import build_list

from .war_member import WarMember

class WarClan(BaseClan, MemberContainer):
    """
    A representation of a clan in war. 
    """
    
    __slots__ = (
        'war',

        'attacks_used',
        'stars_gained',
        'destruction_caused',
        '__member_dict',

        'is_league_war'
    )

    def __init__(self, data, war, is_league_war=False):
        super().__init__(data)
        
        # War is currently unbuilt and probably shouldn't be used other than a reference
        self.war = war

        self.attacks_used:int = data.get('attacks', 0)
        self.stars_gained:int = data.get('stars', 0)
        self.destruction_caused:float = data.get('destructionPercentage', 0)
        
        self.__member_dict = dict({
            mdata.get('tag'): WarMember(data) for mdata in data.pop('members', [])
        })
        #self.members:Tuple[WarMember] = tuple(build_list(data.get('members', []), WarMember))

        self.is_league_war = is_league_war

    @property
    def members(self) -> List[WarMember]:
        return list(self.__member_dict.values())
    
    @property
    def attacks_left(self):
        return (self.war.team_size * 1 if self.is_league_war else 1) - self.attacks_used