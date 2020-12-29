import datetime
from typing import Tuple

from .abc import BaseClan, Tagable, ClashObject
from .enums import WarState

from .utils import build_list, format_time, execute_if_found

# Special information stored inside "attacks" inside a member "members" of WarClan participants
class WarAttack(ClashObject):
    __slots__ = (
        'attacker', # Should attacker and defender be tags or player objects?
        'defender',
        'stars',
        'destruction',
        'order'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} attacker={0.attacker}, defender={0.defender}, stars={0.stars}, destruction={0.destruction}>'.format(self)

    def __init__(self, data):
        self.attacker = data.get('attackerTag') # Currently only a tag
        self.defender = data.get('defenderTag') # Currently only a tag
        self.stars = data.get('stars')
        self.destruction = data.get('destructionPercentage')
        self.order = data.get('order')


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
        self.attacks:Tuple[WarAttack] = tuple(build_list(data.get('attacks', []), WarAttack))
        self.best_opponent_attack: WarAttack = WarAttack(data.get('bestOpponentAttack', {})) # Could be null

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


# Defines a war in Clash
class War(ClashObject):
    __slots__ = (
        'state',

        'team_size',
        'preparation_start',
        'battle_start',
        'battle_end',
        'team_one',
        'team_two'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} team_one={0.team_one} team_two={0.team_two}>'.format(self)

    def __init__(self, data):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self.state = WarState.from_data(data.get('state')) # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self.team_size = data.get('teamSize', 0),
        self.preparation_start = execute_if_found(data, 'preparationStartTime', format_time, default=datetime.datetime.min)
        self.battle_start = execute_if_found(data, 'startTime', format_time, default=datetime.datetime.min)
        self.battle_end = execute_if_found(data, 'endTime', format_time, default=datetime.datetime.min)

        # Team order will always be the same, no matter what clan was requested
        self.team_one = WarClan(data.get('clan'), self)
        self.team_two = WarClan(data.get('opponent'), self)

