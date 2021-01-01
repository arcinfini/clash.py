from typing import List

from .abc import BaseUser, Tagable
from .misc import League, Achievement, Troop
from .utils import build_list, search, collect

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

        self.__achievement_list = list(
            Achievement(achievement_data) for achievement_data in data.get('achievements')
        ) # Achievment data (should be dict?)
        self.__troop_list = list(
            Troop(troop_data) fortroop_data in data.get('troops')
        ) # Maybe later sort by hero, troop and spell

    # def __init_achievements_list could be used to keep __achievements_list as generator and init it when need to preserve ram

    @property
    def achievements(self) -> List[Achievement]:
        return self.__achievements_list.copy()

    @property
    def troops(self) -> List[Troop]:
        return self.__troop_list.copy()

    def search_achievement(self, **attrs) -> Optional[Achievement]:
        r"""Returns the first `Achievement` found based on attributes passed

        Example
        -------

            user = await clientl.fetch_user(user_tag, cls=ProfileUser)
            achievement = user.search_achievement(stars=3)

        Parameters
        ----------
        attrs : 
            The attribute-value pairs of what to search for

        Returns
        -------
        The achievements that matches the attributes: `Optional[Achievement]`
        """

        return search(self.__achievement_list, **attrs)

    def get_achievement(self, name:str) -> Optional[Achievement]:
        """Gets the `Achievement` with the name that matches the string provided

        This method is a shorthand for..
            using user.search_achievement(name='achievement name')

        Parameters
        ==========

        """
        return self.search_achievement(name=name)

    def collect_achievements(self, predicate=None, **attrs):
        """Collects a list of `Achievements` that meet the predicate 
        or attributes passed and returns the result

        This method is a shorthand for..

            achievements = utils.collect(user.achievements, predicate)
        or
            achievements = utils.collect(user.achievements, **attributes)

        Parameters
        ==========
        predicate : `Callable[[Achievement], bool]`
            A callable meant to determine if an achievement should be collected
        attrs : 
            The attribute-value pair of what to collect

        Returns
        -------
        A list of members that meet the predicate or attributes: List[ClanMember]
        """
        return collect(self.__achievement_list, predicate, **attrs)

    # get_troop
    def get_troop(self, name:str) -> Troop:
        return search(self.__troop_list, name=name)

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
        self.clan_rank = data.get('clanRank', None)
        self.previous_clan_rank = data.get('previousClanRank')
        self.donations = data.get('donations')
        self.donations_received = data.get('donationsReceived')
        
        self.clan = clan

    @property
    def rank_delta(self) -> int:
        """`int`: The change in the members clan rank over the current season"""
        return self.clan_rank - self.previous_clan_rank
