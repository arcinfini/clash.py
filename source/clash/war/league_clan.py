from clash.abc import BaseClan, MemberContainer
from .league_member import LeagueMember

class LeagueClan(BaseClan, MemberContainer):
    __slots__ = ('__member_dict')

    def __init__(self, data):
        self.__member_dict = dict({
            mdata.get('tag'): LeagueMember(mdata, league_group=self) for mdata in data.pop('members', [])
        })

        super().__init__(data)

    @property
    def members(self):
        return list(self.__member_dict.values())