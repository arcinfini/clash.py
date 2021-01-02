from clash.abc import Tagable

class LeagueMember(Tagable):
    __slots__ = ('th_level', 'league_group')

    def __init__(self, data, league_group):
        self.th_level = data.pop('townHallLevel', 0)
        self.league_group = league_group

        super().__init__(data.get('tag'), data.get('name'))