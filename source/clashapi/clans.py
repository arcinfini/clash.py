from typing import List

from .abc import BaseClan
from .users import ClanMember
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
        '_war_leage',
        '_member_count',
        '_members'
    )

    def __init__(self, data):
        super().__init__(data)

        self._type = data.get('type') # has enum type
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
        self._war_leage = data.get('warLeague')
        self._member_count = data.get('members')
        self._members = build_list(data.get('memberList'), ClanMember, clan=self) # Unparsed list of ClanMember info

    def __repr__(self):
        return f"<{self.__class__.__name__} tag={self._tag}, name={self._name}>"

# class LeaugeClan(WarClan):
#     pass