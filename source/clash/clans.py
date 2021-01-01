from typing import List, Union, Optional

from .abc import BaseClan
from .users import ClanMember, User
from .enums import ClanType
from .utils import search, find, collect, correct_tag

class Clan(BaseClan):
    __slots__ = (
        'type',
        'description',
        'points',
        'versus_points',
        'required_trophies',
        'war_frequency',
        'war_win_streak',
        'war_wins',
        'war_ties',
        'war_losses',
        'public_war_log',
        'war_league',
        'member_count',
        '__member_list'
    )

    def __init__(self, data):
        super().__init__(data)

        self.type = ClanType.from_data(data.get('type')) # has enum type
        self.description = data.get('description')
        

        self.points = data.get('clanPoints')
        self.versus_points = data.get('clanVersusPoints')
        self.required_trophies = data.get('requiredTrophies')
        self.war_frequency = data.get('warFrequency') # can be turned into an enum
        self.war_win_streak = data.get('warWinStreak')
        self.war_wins = data.get('warWins')
        self.war_ties = data.get('warTies')
        self.war_losses = data.get('warLosses')
        self.public_war_log = data.get('isWarLogPublic')
        self.war_league = data.get('warLeague') # Build class of data
        self.member_count = data.get('members')
        
        self.__member_list = list(
            ClanMember(member_data, clan=self) for member_data in data.get('memberList', [])
        )

    @property
    def members(self) -> List[ClanMember]:
        """List[`ClanMember`]: A list of the clanmembers"""
        return self.__member_list.copy()

    @property
    def is_full(self) -> bool:
        """`bool`: returns if member_count is the size of a max clan"""
        return self.member_count == 50

    def get_member(self, tag:str) -> Optional[ClanMember]:
        """Gets the `ClanMember` with the tag that matches the tag provided
        
        Example
        -------
        
            clan = await client.fetch_clan('clan_tag')
            member = clan.get_member('player_tag')

        Returns
        -------
        The member with a matching tag: Optional[`ClanMember`]
        """
        tag = correct_tag(tag)
        return find(self.__member_list, lambda x: x.tag == tag)

    def search_member(self, **attributes) -> Optional[ClanMember]:
        """Returns the first found `ClanMember` that meets the attributes passed
        
        Example
        -------
        
            clan = await client.fetch_clan('clan_tag')
            member = clan.search_member(name='user name')

        Returns
        -------
        The member found: Optional[`ClanMember`]
        """
        return search(self.__member_list, **attributes)

    def collect_members(self, predicate=None, **attrs) -> List[ClanMember]:
        """Returns a list of `ClanMembers` that meet the predicate or attributes passed

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
        return collect(self.__member_list, predicate, **attrs)

# class LeaugeClan(WarClan):
#     pass