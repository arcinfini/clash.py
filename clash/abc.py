import abc
import typing

from .utils import protected, collect, search
from .misc import League

@protected
class ClashObject(object):
    def __init_subclass__(cls, *args, **kwargs):
        return protected(cls)

class Tagable(ClashObject):
    """Represents objects that have a tag and name associated with them"""

    __slots__ = ('tag', 'name')
    
    def __repr__(self):
        return "<{0.__class__.__name__} tag={0.tag}, name={0.name}>".format(self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.tag == other.tag

    def __init__(self, tag, name):
        self.tag = tag
        self.name = name

class BaseUser(Tagable): # A representation that all users must meet
    """A BaseUser inherited by other user classes.

    """
    
    __slots__ = (
        'exp_level',
        'trophies',
        'versus_trophies',

        'league',

        'client'
    )

    def __init__(self, data, client):
        self.exp_level:int = data.get('expLevel')
        self.trophies:int = data.get('trophies')
        self.versus_trophies:int = data.get('versusTrophies')
        self.league = League(**data.get('league'))

        self.client = client

        super().__init__(data.get('tag'), data.get('name'))


class BaseClan(Tagable):
    __slots__ = (
        'badge_urls',
        'level',

        'client'
    )

    def __init__(self, data, client):
        self.badge_urls = data.get('badgeUrls')
        self.level = data.get('clanLevel')
        
        self.client = client

        super().__init__(data.get('tag'), data.get('name'))

# Later could be implemented if multiple types of containers pop up
# class Container(abc.ABC):

#     @property
#     @abc.abstractmethod
#     def _contained_(self): ...

class MemberContainer(abc.ABC):
    """An ABC mean to host methods for classes that contain a list/dict of members
    """
    @property
    @abc.abstractmethod
    def members(self) -> typing.List[BaseUser]: 
        """List[`BaseUser`]: A list of users that are contained within the container"""
        raise NotImplementedError

    def search_member(self, **attributes) -> typing.Optional[BaseUser]:
        """Returns the first found user that meets the attributes passed
        
        Example
        -------
        
            clan = await client.fetch_clan('clan_tag')
            member = clan.search_member(name='user name')

        Returns
        -------
        The member found: Optional[`BaseUser`]
        """
        return search(self.members, **attributes)

    def collect_members(self, predicate=None, **attrs) -> typing.List[BaseUser]:
        """Returns a list of users that meet the predicate or attributes passed

        If a predicate is passed then the attributes are ignored

        Examples
        --------
            # collects all coleaders
            clan = await client.fetch_clan('clan_tag')
            members = clan.collect_members(role='coleader')

        or

            # collects the top ten members
            clan = await client.fetch_clan('clan_tag')
            members = clan.collect_members(lambda m: m.clan_rank >= 10)

        Returns
        -------
        A list of members that meet the predicate or attributes: List[ClanMember]
        """
        return collect(self.members, predicate, **attrs)

class ClanContainer(abc.ABC):
    
    @property
    @abc.abstractmethod
    def clans(self) -> typing.List[BaseClan]:
        """List[`BaseClan`]: A list of clans that are contained within the container"""
        raise NotImplementedError

    def search_clan(self, **attributes) -> typing.Optional[BaseClan]:
        """
        """

        return search(self.clans, **attributes)

    def collect_clans(self, predicate=None, **attributes) -> typing.List[BaseClan]:
        """
        """

        return collect(self.clans, predicate, **attributes)