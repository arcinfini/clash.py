
class BaseUser: # A representation that all users must meet
    __slots__ = (
        '_tag',
        '_name',

        '_exp_level',
        '_trophies',
        '_versus_trophies',

        '_league'
    )

    def __init__(self, data):
        self._tag = data['tag']
        self._name = data['name']
        self._exp_level = data['expLevel']
        self._trophies = data['trophies']
        self._versus_trophies = data['versusTrophies']
        self._league = data['league'] # Raw league data, create League class

class User(BaseUser): # A representation of a base player profile
    __slots__ = (
        '_th_level',
        
        '_best_trophies',
        '_war_stars',
        '_attack_wins',
        '_defense_wins',
        
        '_builder_hall_level',
        '_best_versus_trophies',
        '_versus_wins'

        # '_clan'
        # clan will not always exist if the user is not
        # in a clan, there is no way to account for this
        # yet even though it is easy to do so
        # however implement this later
    )

    def __init__(self, data):
        super().__init__(data)

        self._th_level
        self._best_trophies
        self._war_stars
        self._attack_wins
        self._defense_wins
        self._builder_hall_level
        self._best_versus_trophies
        self._versus_wins

class ProfileUser(User):
    __slots__ = (
        '_achievements',
        '_troops'
    )

    def __init__(self, data):
        super().__init__(data)

        self._achievements = data['achievements']
        self._troops = data['troops']

class ClanMember(BaseUser):
    __slots__ = (
        '_role', # leader, coleader, admin, member
        '_clan_rank',
        '_previous_clan_rank',
        '_donations',
        '_donations_received',

        '_clan'
    )

    def __init__(self, data, clan=None):
        super().__init__(data)

        self._role = data['role']
        self._clan_rank = data['clanRank']
        self._previous_clan_rank = data['previousClanRank']
        self._donations = data['donations']
        self._donations_received = data['donationsReceived']
        
        self._clan = clan

class WarMember: # Extend baseUser or clanmember or be separate
    __slots__ = (
        '_tag',
        '_name',
        '_th_level'
        '_map_position',
        '_attacks'

        # defences,
        # best opponent attack
    )

    def __init__(self, data):
        self._tag = data['tag']
        self._name = data['name']
        self._th_level = data['townhallLevel']
        self._map_position = data['mapPosition']
        self._attacks = data['attacks'] # Raw WarAttack list
