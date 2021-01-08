from typing import List, Optional

from .abc import BaseUser, BaseClan, Tagable
from .enums import ClanRole
from .misc import League, Achievement, Troop, Hero, Spell
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

        '_clan' # Will not always exists
    )

    def __init__(self, data, client):
        super().__init__(data, client)

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
            self._clan = BaseClan(_clan, client=client)
        else: self._clan = None


class ProfileUser(User):
    """
    A higher level user class that has representation for achievements and troops
    """
    
    __slots__ = (
        '__achievement_dict',

        '__troop_dict',

        '__hero_dict',

        '__spell_dict',
    )

    def _build(self, cls, data, get):
        return dict({
            cls_data.get('name'): cls(cls_data) for cls_data in data.pop(get, [])
        })

    def __init__(self, data, client):
        super().__init__(data, client)

        self.__achievement_dict = self._build(Achievement, data, 'achievements')
        self.__troop_dict = self._build(Troop, data, 'troops')
        self.__hero_dict = self._build(Hero, data, 'heroes')
        self.__spell_dict = self._build(Spell, data, 'spells')

    # def __init_achievements_list could be used to keep __achievement_list as generator and init it when need to preserve ram

    @property
    def achievements(self) -> List[Achievement]:
        """List[`Achievement`]: A list of the user's achievements"""
        
        return self.__achievement_dict.values()

    @property
    def troops(self) -> List[Troop]:
        """List[`Troop`]: A list of the user's troops"""

        return self.__troop_dict.values()

    @property
    def heroes(self) -> List[Hero]:
        """List[`Hero`]: A list of the user's heroes"""
        
        return self.__hero_list.values()

    @property
    def spells(self) -> List[Spell]:
        """List[`Spell`]: A list of the user's spells"""
        
        return self.__spell_list.values()

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

        return search(self.__achievement_dict.values(), **attrs)

    def get_achievement(self, name:str) -> Optional[Achievement]:
        """Gets the `Achievement` with the name that matches the string provided

        This method is a shorthand for using..
            user.search_achievement(name='achievement name')

        Parameters
        ==========
        name : `str`
            The name of the achievement.

        Returns
        -------
        The achievement with the matching name: `Achievemnt`
        """
        # Doesnt need to init achievements because it should be done in search_achievement
        return self.__achievement_dict.get(name, None)

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
        A list of achievements that meet the predicate or attributes: List[Achievement]
        """

        return collect(self.__achievement_dict.values(), predicate, **attrs)

    # get_troop
    def get_troop(self, name:str) -> Troop:
        """Gets the `Troop` with the name that matches the string provided.
        
        Parameters
        ==========
        name : `str`
            The name of the troop

        Returns
        -------
        The troop with the matching name: `Troop`
        """

        return self.__troop_dict.get(name, None)


class ClanMember(BaseUser):
    __slots__ = (
        'role',
        'clan_rank',
        'previous_clan_rank',
        'donations',
        'donations_received',

        'clan'
    )

    def __init__(self, data, client, clan=None):
        super().__init__(data, client)

        self.role = ClanRole.from_value(data.get('role'))
        self.clan_rank:int = data.get('clanRank')
        self.previous_clan_rank:int = data.get('previousClanRank')
        self.donations:int = data.get('donations')
        self.donations_received:int = data.get('donationsReceived')
        
        self.clan = clan

    @property
    def rank_delta(self) -> int:
        """`int`: The change in the members clan rank over the current season"""
        return self.clan_rank - self.previous_clan_rank
