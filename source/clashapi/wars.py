import datetime

from .abc import BaseClan
from .enums import WarState

from .utils import build_list, format_time

class WarClan(BaseClan):
    """
    A representation of a clan in war. 
    """
    
    __slots__ = (
        '_war',

        '_attacks_used',
        '_stars_gained',
        '_destruction_caused',
        '_participants'
    )

    def __init__(self, data, war):
        super().__init__(data)
        
        # War is currently unbuilt and probably shouldn't be used other than a reference
        self._war = war

        self._attacks_used:int = data.get('attacks')
        self._stars_gained:int = data.get('stars')
        self._destruction_caused:float = data.get('destructionPercentage')
        self._participants:List[WarMember] = build_list(data.get('members'), WarMember)


# Defines a war in Clash
class War:
    __slots__ = (
        '_state',

        '_team_size',
        '_preparation_start',
        '_battle_start',
        '_battle_end',
        '_team_one',
        '_team_two'
    )

    def __repr__(self):
        return f'<{self.__class__.__name__} team_one={self.team_one} team_two={self.team_two}>'

    def __init__(self, data):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self._state = WarState.from_data(data.get('state')) # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self._team_size = data.get('teamSize'),
        self._preparation_start = format_time(data.get('preparationStartTime'))
        self._battle_start = format_time(data.get('startTime'))
        self._battle_end = format_time(data.get('endTime'))

        # Team order will always be the same, no matter what clan was requested
        self._team_one = WarClan(data.get('clan'), self)
        self._team_two = WarClan(data.get('opponent'), self)

    @property
    def state(self) -> WarState:
        return self._state

    @property
    def prep_start(self) -> datetime.datetime:
        return self._preparation_start

    @property
    def battle_start(self) -> datetime.datetime:
        return self._battle_start

    @property
    def battle_end(self) -> datetime.datetime:
        return self._battle_end

    @property
    def team_one(self) -> WarClan:
        return self._team_one

    @property
    def team_two(self) -> WarClan:
        return self._team_two

    @property
    def team_size(self) -> int:
        return self._team_size


# Special information stored inside "attacks" inside a member "members" of WarClan participants
class WarAttack:
    __slots__ = (
        '_attacker', # Should attacker and defender be tags or player objects?
        '_defender',
        '_stars',
        '_destruction',
        '_order'
    )

    def __init__(self, data):
        self._attacker = data.get('attacker') # Currently only a tag
        self._defender = data.get('defender') # Currently only a tag
        self._stars = data.get('stars')
        self._destruction = data.get('destructionPercentage')
        self._order = data.get('order')


class WarMember:
    __slots__ = (
        '_tag',
        '_name',
        '_th_level',
        '_map_position',
        '_attacks', #  Attacks will appear null if they haven't attacked yet

        '_best_opponent_attack' # Could also be null if no defences
        # defences, 
        # opponentAttacks
    )

    def __init__(self, data):
        self._tag:str = data.get('tag')
        self._name:str = data.get('name')
        self._th_level:int = data.get('townhallLevel')
        self._map_position:int = data.get('mapPosition')
        self._attacks:List[WarAttack] = build_list(data.get('attacks', []), WarAttack)
        self._best_opponent_attack: WarAttack = WarAttack(data.get('bestOpponentAttack', {})) # Could be null