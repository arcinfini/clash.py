import typing

from .utils import protected

@protected
class ClashTag:
    __slots__ = ('tag')

    @staticmethod
    def fix(tag:str):
        stripped = tag.strip(' ')
        return f'{"#" if not stripped.startswith("#") else ""}{stripped}'

    def __init__(self, tag, **kwargs):
        self.tag = ClashTag.fix(tag)

    def __str__(self):
        return self.tag

    def __eq__(self, other):
        # Users and Clans can have the same tag this might not be an ideal way to store a tag
        return isinstance(other, self.__class__) and self.tag == other.tag

"""
"league": {
    "name": {},
    "id": 0,
    "iconUrls": {}
"""

@protected
class League:
    __slots__ = (
        'name',
        'id',
        'icons'
    )

    def __init__(self, name:str, id:int, icon_urls=None, **kwargs):
        self.name = name
        self.id = id
        self.icons = icon_urls

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id


class WarLeague:
	__slots__ = ("name", "id")

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.id == other.id

	def __init__(self, data={}):
		self.name = data.pop("name", 'Unknown')
		self.id = data.pop("id", 0)

"""
"labels": [
      {
        "name": {},
        "id": 0,
        "iconUrls": {}
      }

"""

@protected
class Label:
    __slots__ = (
        'name',
        'id',
        'icons'
    )

    def __init__(self, name:str, id:int, icon_urls=None, **kwargs):
        self.name = name
        self.id = id
        self.icons = icon_urls

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

""" While this exists, i see no purpose for the knowledge of this data
"location": {
		"localizedName": "string",
		"id": 0,
		"name": "string",
		"isCountry": true,
		"countryCode": "string"
    }
"""

""" Decently important but not critical
legendStatistics": {
    "bestSeason": {
		"trophies": 0,
		"id": "string",
		"rank": 0
    },
    "currentSeason": {
		"trophies": 0,
		"id": "string",
		"rank": 0
    },
    "previousSeason": {
		"trophies": 0,
		"id": "string",
		"rank": 0
    },
    "previousVersusSeason": {
		"trophies": 0,
		"id": "string",
		"rank": 0
    },
    "bestVersusSeason": {
		"trophies": 0,
		"id": "string",
		"rank": 0
    },
    "legendTrophies": 0
  },
"""



"""
"troops": [
    {
		"level": 0,
		"name": {},
		"maxLevel": 0,
		"village": "string"
    }
  ],
  "heroes": [
    {
		"level": 0,
		"name": {},
		"maxLevel": 0,
		"village": "string"
    }
  ],
  "spells": [
    {
		"level": 0,
		"name": {},
		"maxLevel": 0,
		"village": "string"
    }
  ],
"""

@protected
class Troop:
    __slots__ = (
        'level',
        'name',
        'max_level',
        'village',
    )

    def __repr__(self):
        return "<{0.__class__.__name__} name={0.name}, level={0.level}>".format(self)

    def __init__(self, data=None, **kwargs):
        self.level = data.get('level', 0)
        self.name = data.get('name', 'Unknown')
        self.max_level = data.get('maxLevel', 0)
        self.village = data.get('village', 'Unknown')

    @property
    def is_max(self):
        return self.max_level == self.level

    # Return true based on village value
    # @property
    # def is_main_village(self):
    #     return None

class Hero(Troop):
    pass

class Spell(Troop):
    pass

@protected
class Achievement:
    __slots__ = (
        'name',
        'stars',
        'value',
        'target',
        'info',
        'completion_info',
        'village' # should become an enum
    )

    def __repr__(self):
        return "<{0.__class__.__name__} name={0.name}, stars={0.stars}>".format(self)

    def __init__(self, data=None, **kwargs):
        self.name = data.get('name', 'Unknown')
        self.stars = data.get('stars', 0)
        self.value = data.get('value', 0)
        self.target = data.get('target', 0)
        self.info = data.get('info', 'Unknown')
        self.completion_info = data.get('completionInfo', 'Unknown')
        self.village = data.get('village', 'Unknown')