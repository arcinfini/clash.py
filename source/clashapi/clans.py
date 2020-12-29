from typing import List

from .abc import BaseClan
from .users import ClanMember
from .enums import ClanType
from .utils import build_list

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
        'members'
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
        self.members = build_list(data.get('memberList'), ClanMember, clan=self)

# class LeaugeClan(WarClan):
#     pass