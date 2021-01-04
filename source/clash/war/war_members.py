from clash.abc import Tagable
from clash.utils import build_list

from .war_attack import WarAttack

class WarMember(Tagable):
    """Represents a member of a clan in a War"""

    __slots__ = (
        'th_level',
        'map_position',
        'attacks', #  Attacks will appear null if they haven't attacked yet

        'best_opponent_attack', # Could also be null if no defences
        # defences, 
        # opponentAttacks

        'client'
    )

    def __init__(self, data, client):
        self.th_level:int = data.get('townhallLevel')
        self.map_position:int = data.get('mapPosition')
        self.attacks = tuple(build_list(data.get('attacks', []), WarAttack))
        self.best_opponent_attack = WarAttack(data.get('bestOpponentAttack', {}), client=client) # Could be null

        self.client = client

        super().__init__(data.get('tag'), data.get('name'))


class LeagueMember(Tagable):
    """Represents a member of a clan in a LeagueGroup"""

    __slots__ = ('th_level', 'league_group')

    def __init__(self, data, league_group):
        self.th_level = data.pop('townHallLevel', 0)
        self.league_group = league_group

        super().__init__(data.get('tag'), data.get('name'))