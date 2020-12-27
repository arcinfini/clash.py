from .misc import League

class Tagable:
    __slots__ = ('_tag', '_name')
    
    def __repr__(self):
        return f"<{self.__class__.__name__} tag={self._tag}, name={self._name}>"

    def __init__(self, tag, name):
        self._tag = tag
        self._name = name

    @property
    def tag(self) -> str:
        return self._tag

    @property
    def name(self) -> str:
        return self._name

class BaseUser(Tagable): # A representation that all users must meet
    """
    A BaseUser inherited by other user classes.

    """
    
    __slots__ = (
        '_exp_level',
        '_trophies',
        '_versus_trophies',

        '_league'
    )

    def __init__(self, data):
        self._exp_level:int = data.get('expLevel')
        self._trophies:int = data.get('trophies')
        self._versus_trophies:int = data.get('versusTrophies')
        self._league = League(**data.get('league'))

        super().__init__(data.get('tag'), data.get('name'))

    @property
    def exp_level(self) -> int:
        return self._exp_level

    @property
    def trophies(self) -> int:
        return self._trophies

    @property
    def versus_trophies(self) -> int:
        return self._versus_trophies
    
    @property
    def league(self) -> League:
        return self._league


class BaseClan(Tagable):
    __slots__ = (
        '_badge_urls',
        '_level'
    )

    def __init__(self, data):
        self._badge_urls = data.get('badgeUrls')
        self._level = data.get('clanLevel')

        super().__init__(data.get('tag'), data.get('name'))