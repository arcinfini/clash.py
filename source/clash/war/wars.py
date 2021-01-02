import datetime
from typing import Tuple

from clash.abc import BaseClan, ClashObject
from clash.enums import WarState
from clash.utils import build_list, format_time, execute_if_found

from .war_clan import WarClan

# Defines a war in Clash
class War(ClashObject):
    __slots__ = (
        'state',

        'team_size',
        'preparation_start',
        'battle_start',
        'battle_end',
        'team_one',
        'team_two',

        'client'
    )

    def __repr__(self):
        return '<{0.__class__.__name__} team_one={0.team_one} team_two={0.team_two}>'.format(self)

    def __init__(self, data, client):
        # In future, potentially - extract_data(self, data) - remember self.__class__
        self.state = WarState.from_data(data.get('state')) # This may later turn into an enum like value instead of a string

        # If state means not in war, should the information end here?

        self.team_size = data.get('teamSize', 0),
        self.preparation_start = execute_if_found(data, 'preparationStartTime', format_time, default=datetime.datetime.min)
        self.battle_start = execute_if_found(data, 'startTime', format_time, default=datetime.datetime.min)
        self.battle_end = execute_if_found(data, 'endTime', format_time, default=datetime.datetime.min)

        self.client = client

        # Team order will always be the same, no matter what clan was requested
        self.team_one = WarClan(data.get('clan'), client, self)
        self.team_two = WarClan(data.get('opponent'), client, self)

