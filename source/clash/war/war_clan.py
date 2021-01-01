
from clash.abc import BaseClan
from clash.utils import build_list

from .war_member import WarMember

class WarClan(BaseClan):
    """
    A representation of a clan in war. 
    """
    
    __slots__ = (
        'war',

        'attacks_used',
        'stars_gained',
        'destruction_caused',
        'participants'
    )

    def __init__(self, data, war):
        super().__init__(data)
        
        # War is currently unbuilt and probably shouldn't be used other than a reference
        self.war = war

        self.attacks_used:int = data.get('attacks', 0)
        self.stars_gained:int = data.get('stars', 0)
        self.destruction_caused:float = data.get('destructionPercentage', 0)
        self.participants:Tuple[WarMember] = tuple(build_list(data.get('members', []), WarMember))

    @property
    def attacks_left(self):
        return self.war.team_size - self.attacks_used