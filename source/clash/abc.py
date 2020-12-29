from .utils import protected
from .misc import League

@protected
class ClashObject(object):
    def __init_subclass__(cls, *args, **kwargs):
        return protected(cls)

class Tagable(ClashObject):
    __slots__ = ('tag', 'name')
    
    def __repr__(self):
        return "<{0.__class__.__name__} tag={0.tag}, name={0.name}>".format(self)

    def __init__(self, tag, name):
        self.tag = tag
        self.name = name

class BaseUser(Tagable): # A representation that all users must meet
    """
    A BaseUser inherited by other user classes.

    """
    
    __slots__ = (
        'exp_level',
        'trophies',
        'versus_trophies',

        'league'
    )

    def __init__(self, data):
        self.exp_level:int = data.get('expLevel')
        self.trophies:int = data.get('trophies')
        self.versus_trophies:int = data.get('versusTrophies')
        self.league = League(**data.get('league'))

        super().__init__(data.get('tag'), data.get('name'))


class BaseClan(Tagable):
    __slots__ = (
        'badge_urls',
        'level'
    )

    def __init__(self, data):
        self.badge_urls = data.get('badgeUrls')
        self.level = data.get('clanLevel')

        super().__init__(data.get('tag'), data.get('name'))