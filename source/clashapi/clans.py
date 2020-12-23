
class BaseClan:
    __slots__ = (
        '_tag',
        '_name',
        '_badge_urls',
        '_level'
    )

    def __init__(self, data):
        self._tag = data['tag']
        self._name = data['name']
        self._badge_urls = data['badgeUrls']
        self._level = data['clanLevel']

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

        self._type = data['type'] # has enum type
        self._description = data['description']
        

        self._points = data.get('clanPoints')
        self._versus_points = data['clanVersusPoints']
        self._required_trophies = data['requiredTrophies']
        self._war_frequency = data['warFrequency'] # can be turned into an enum
        self._war_win_streak = data['warWinStreak']
        self._war_wins = data['warWins']
        self._war_ties = data['warTies']
        self._war_losses = data['warLosses']
        self._public_war_log = data['isWarLogPublic']
        self._war_leage = data['warLeague']
        self._member_count = data['members']
        self._members = data['memberList'] # Unparsed list of ClanMember info

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

        self._attacks_used = data['attacks']
        self._stars_gained = data['stars']
        self._destruction_caused = data['destructionPercentage']
        self._participants = data['members'] # This information is unparsed WarMember info

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
        self._state = data['state'] # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self._team_size = data['teamSize'],
        self._preparation_start = data['preparationStartTime']
        self._battle_start = data['startTime']
        self._end = data['endTime']

        # Team order will always be the same, no matter what clan was requested
        self._team_one = WarClan(data['clan'], self)
        self._team_two = WarClan(data['opponent'], self)

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
        self._attacker = data['attacker'] # Currently only a tag
        self._defender = data['defender'] # Currently only a tag
        self._stars = data['stars']
        self._destruction = data['destructionPercentage']
        self._order = data['order']

"""
Python Enum

Enum : notInWar, inWar
"""