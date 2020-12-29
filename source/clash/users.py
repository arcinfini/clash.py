from typing import List

from .abc import BaseUser, Tagable
from .misc import League, Achievement, Troop
from .utils import build_list

class User(BaseUser): # A representation of a base player profile
    __slots__ = (
        'th_level',
        
        'best_trophies',
        'war_stars',
        'attack_wins',
        'defense_wins',
        
        'builder_hall_level',
        'best_versus_trophies',
        'versus_wins',

        'clan' # Will not always exists
    )

    def __init__(self, data):
        super().__init__(data)

        self.th_level = data.get('townHallLevel')
        self.best_trophies = data.get('bestTrophies')
        self.war_stars = data.get('warStars')
        self.attack_wins = data.get('attackWins')
        self.defense_wins = data.get('defenceWins')
        self.builder_hall_level = data.get('builderHallLevel', 0)
        self.best_versus_trophies = data.get('bestVersusTrophies', 0)
        self.versus_wins = data.get('versusWins', 0)

        _clan = data.get("clan", None)
        if _clan is not None:
            self._clan = BaseClan(_clan)
        else: self._clan = None

class ProfileUser(User):
    """
    A higher level user class that has representation for achievements and troops
    """
    
    __slots__ = (
        'achievements',
        'troops'
    )

    def __init__(self, data):
        super().__init__(data)

        self.achievements = build_list(data.get('achievements'), Achievement) # Achievment data (should be dict?)
        self.troops = build_list(data.get('troops'), Troop) # Raw Troop data

class ClanMember(BaseUser):
    __slots__ = (
        'role', # leader, coleader, admin, member
        'clan_rank',
        'previous_clan_rank',
        'donations',
        'donations_received',

        'clan'
    )

    def __init__(self, data, clan=None):
        super().__init__(data)

        self.role = data.get('role')
        self.clan_rank = data.get('clanRank')
        self.previous_clan_rank = data.get('previousClanRank')
        self.donations = data.get('donations')
        self.donations_received = data.get('donationsReceived')
        
        self.clan = clan
