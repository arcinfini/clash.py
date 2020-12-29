from typing import List

from .abc import BaseClan
from .users import ClanMember
from .enums import ClanType
from .utils import build_list

class Clan(BaseClan):
    __slots__ = (
        '_type',
        '_description',
        '_points',
        '_versus_points',
        '_required_trophies',
        '_war_frequency',
        '_war_win_streak',
        '_war_wins',
        '_war_ties',
        '_war_losses',
        '_public_war_log',
        '_war_league',
        '_member_count',
        '_members'
    )

    def __init__(self, data):
        super().__init__(data)

        self._type = ClanType.from_data(data.get('type')) # has enum type
        self._description = data.get('description')
        

        self._points = data.get('clanPoints')
        self._versus_points = data.get('clanVersusPoints')
        self._required_trophies = data.get('requiredTrophies')
        self._war_frequency = data.get('warFrequency') # can be turned into an enum
        self._war_win_streak = data.get('warWinStreak')
        self._war_wins = data.get('warWins')
        self._war_ties = data.get('warTies')
        self._war_losses = data.get('warLosses')
        self._public_war_log = data.get('isWarLogPublic')
        self._war_league = data.get('warLeague') # Build class of data
        self._member_count = data.get('members')
        self._members = build_list(data.get('memberList'), ClanMember, clan=self)
    
    @property
    def points(self) -> int:
        return self._points
    
    @property
    def versus_points(self) -> int:
        return self._versus_points

    @property
    def required_trophies(self) -> int:
        return self._required_trophies

    @property
    def war_frequency(self) -> str:
        return self._war_frequency

    @property
    def war_win_streak(self) -> int:
        return self._war_win_streak

    @property
    def war_wins(self) -> int:
        return self._war_wins

    @property
    def war_ties(self) -> int:
        return self._war_ties

    @property
    def war_losses(self) -> int:
        return self._war_losses

    @property
    def public_war_log(self) -> bool:
        return self._public_war_log

    @property
    def war_league(self):
        pass

    @property
    def member_count(self) -> int:
        return self._member_count

    @property
    def members(self) -> List[ClanMember]:
        return self._members

# class LeaugeClan(WarClan):
#     pass