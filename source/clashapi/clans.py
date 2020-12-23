
class BaseClan:
    __slots__ = (
        '_tag',
        '_name',
        '_badge_urls',
        '_level'
    )

    def __init__(self, data):
        self._tag = data.get('tag')
        self._name = data.get('name')
        self._badge_urls = data.get('badgeUrls')
        self._level = data.get('clanLevel')

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
        self._members = data.get('memberList') # Unparsed list of ClanMember info

    def __repr__(self):
        return f"<{self.__class__.__name__} tag={self._tag}, name={self._name}>"
    

class WarClan(BaseClan):
    """
    A representation of a clan in war. 
    """
    
    __slots__ = (
        '_war',

        '_attacks_used',
        '_stars_gained',
        '_destruction_caused',
        '_participants'
    )

    def __init__(self, data, war):
        super().__init__(data)
        
        # War is currently unbuilt and probably shouldn't be used other than a reference
        self._war = war

        self._attacks_used = data.get('attacks')
        self._stars_gained = data.get('stars')
        self._destruction_caused = data.get('destructionPercentage')
        self._participants = data.get('members') # This information is unparsed WarMember info

# Will most likely be relocated later

# Defines a war in Clash
class War:
    __slots__ = (
        '_state',

        '_team_size',
        '_preparation_start',
        '_battle_start',
        '_end',
        '_team_one',
        '_team_two'
    )

    def __init__(self, data):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self._state = data.get('state') # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self._team_size = data.get('teamSize'),
        self._preparation_start = data.get('preparationStartTime')
        self._battle_start = data.get('startTime')
        self._end = data.get('endTime')

        # Team order will always be the same, no matter what clan was requested
        self._team_one = WarClan(data.get('clan'), self)
        self._team_two = WarClan(data.get('opponent'), self)

# class LeaugeClan(WarClan):
#     pass

# Special information stored inside "attacks" inside a member "members" of WarClan participants
class WarAttack:
    __slots__ = (
        '_attacker', # Should attacker and defender be tags or player objects?
        '_defender',
        '_stars',
        '_destruction',
        '_order'
    )

    def __init__(self, data):
        self._attacker = data.get('attacker') # Currently only a tag
        self._defender = data.get('defender') # Currently only a tag
        self._stars = data.get('stars')
        self._destruction = data.get('destructionPercentage')
        self._order = data.get('order')

"""
Python Enum

Enum : notInWar, inWar
"""