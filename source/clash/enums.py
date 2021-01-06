from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def from_value(cls, value:str):
        """Searches the referenced Enum for the result of value.upper()
        
        Parameters
        ----------
        value : `str`
            The value to search the enum for

        Returns
        -------
        The enum value corresponding to value.upper()
        """
        try: return cls.__members__[value.upper()]
        except KeyError: raise ValueError(
            "Enum {0.__name__} is outdated or missing value: {1}".format(
                cls.__name__, 
                value
            )
        )

class WarState(BaseEnum):
    NOTINWAR = 0
    PREPARATION = 1
    INWAR = 2
    WARENDED = 3

    @classmethod
    def from_data(cls, value:str):
        """Deprecated, use from_value instead"""
        return super().from_value(value)

class ClanType(BaseEnum):
    CLOSED = 0
    OPEN = 1
    INVITEONLY = 2

    @classmethod
    def from_data(cls, value:str):
        """Deprecated, use from_value instead"""
        return super().from_value(value)


class ClanRole(BaseEnum):
    """An Enum to represent the roles in a clan
    """

    MEMBER = 0
    ADMIN = 1
    ELDER = 1
    COLEADER = 2
    LEADER = 3

    def __gt__(self, other):
        return self.value > other.value

if __name__ == "__main__":
    print(ClanRole.from_value('coleader') < ClanRole.ELDER)
    print(ClanRole.ADMIN)