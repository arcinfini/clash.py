from enum import Enum

class WarState(Enum):
    NOTINWAR = 0
    INWAR = 1

    @classmethod
    def from_data(cls, value:str):
        if value == "notInWar": return cls.NOTINWAR
        elif value == "inWar": return cls.INWAR
        # Should only reach this if the API is changed
        else: raise Exception("Enum WarState is outdated")

class ClanType(Enum):
    CLOSED = 0
    OPEN = 1
    INVITEONLY = 2

    @classmethod
    def from_data(cls, value:str):
        if value == "closed": return cls.CLOSED
        elif value == "open": return cls.OPEN
        elif value == "inviteOnly": return cls.INVITEONLY
        # Should only reach this if the API is changed
        else: raise Exception("Enum ClanType is outdated")