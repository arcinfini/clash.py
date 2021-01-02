from clash.abc import ClashObject

# Special information stored inside "attacks" inside a member "members" of WarClan participants
class WarAttack(ClashObject):
    __slots__ = (
        'attacker', # Should attacker and defender be tags or player objects?
        'defender',
        'stars',
        'destruction',
        'order',

        'client'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} attacker={0.attacker}, defender={0.defender}, stars={0.stars}, destruction={0.destruction}>'.format(self)

    def __init__(self, data, client):
        self.attacker = data.get('attackerTag') # Currently only a tag
        self.defender = data.get('defenderTag') # Currently only a tag
        self.stars = data.get('stars')
        self.destruction = data.get('destructionPercentage')
        self.order = data.get('order')

        self.client = client