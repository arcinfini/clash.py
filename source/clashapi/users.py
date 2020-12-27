from typing import List

from .abc import BaseUser
from .misc import League, Achievement, Troop
from .utils import build_list

class User(BaseUser): # A representation of a base player profile
    __slots__ = (
        '_th_level',
        
        '_best_trophies',
        '_war_stars',
        '_attack_wins',
        '_defense_wins',
        
        '_builder_hall_level',
        '_best_versus_trophies',
        '_versus_wins',

        '_clan' # Will not always exists
    )

    def __init__(self, data):
        super().__init__(data)

        self._th_level = data.get('townHallLevel')
        self._best_trophies = data.get('bestTrophies')
        self._war_stars = data.get('warStars')
        self._attack_wins = data.get('attackWins')
        self._defense_wins = data.get('defenceWins')
        self._builder_hall_level = data.get('builderHallLevel', 0)
        self._best_versus_trophies = data.get('bestVersusTrophies', 0)
        self._versus_wins = data.get('versusWins', 0)

        _clan = data.get("clan", None)
        if _clan is not None:
            self._clan = BaseClan(_clan)
        else: self._clan = None

    @property
    def th_level(self) -> int:
        return self._th_level

    @property
    def best_trophies(self) -> int:
        return self._best_trophies

    @property
    def war_stars(self):
        return self._war_stars

    @property
    def attack_wins(self) -> int:
        return self._attack_wins

    @property
    def defence_wins(self) -> int:
        return self._defense_wins

class ProfileUser(User):
    """
    A higher level user class that has representation for achievements and troops
    """
    
    __slots__ = (
        '_achievements',
        '_troops'
    )

    def __init__(self, data):
        super().__init__(data)

        self._achievements = build_list(data.get('achievements'), Achievement) # Achievment data (should be dict?)
        self._troops = build_list(data.get('troops'), Troop) # Raw Troop data

class ClanMember(BaseUser):
    __slots__ = (
        '_role', # leader, coleader, admin, member
        '_clan_rank',
        '_previous_clan_rank',
        '_donations',
        '_donations_received',

        '_clan'
    )

    def __init__(self, data, clan=None):
        super().__init__(data)

        self._role = data.get('role')
        self._clan_rank = data.get('clanRank')
        self._previous_clan_rank = data.get('previousClanRank')
        self._donations = data.get('donations')
        self._donations_received = data.get('donationsReceived')
        
        self._clan = clan
