from clash.abc import Tagable
from clash.utils import build_list

from .war_attack import WarAttack

class WarMember(Tagable):
    __slots__ = (
        'th_level',
        'map_position',
        'attacks', #  Attacks will appear null if they haven't attacked yet

        'best_opponent_attack' # Could also be null if no defences
        # defences, 
        # opponentAttacks
    )

    def __init__(self, data):
        self.th_level:int = data.get('townhallLevel')
        self.map_position:int = data.get('mapPosition')
        self.attacks = tuple(build_list(data.get('attacks', []), WarAttack))
        self.best_opponent_attack = WarAttack(data.get('bestOpponentAttack', {})) # Could be null

        super().__init__(data.get('tag'), data.get('name'))