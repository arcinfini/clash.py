import typing

from .utils import protected

@protected
class ClashTag:

    @staticmethod
    def fix(tag:str):
        stripped = tag.strip(' ')
        return f'{"#" if not stripped.startswith("#") else ""}{stripped}'

    def __init__(self, tag, **kwargs):
        self._tag = ClashTag.fix(tag)

    @property
    def tag(self):
        return self._tag

    def __str__(self):
        return self.tag

    def __eq__(self, other):
        return self.tag == other.tag

"""
"league": {
    "name": {},
    "id": 0,
    "iconUrls": {}
"""

@protected
class League:
    __slots__ = (
        '_name',
        '_id',
        '_icons'
    )

    def __init__(self, name:str, id:int, icon_urls=None, **kwargs):
        self._name = name
        self._id = id
        self._icons = icon_urls
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

"""
"warLeague": {
    "name": {},
    "id": 0
  }
"""

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
        '_name',
        '_id',
        '_icons'
    )

    def __init__(self, name:str, id:int, icon_urls=None, **kwargs):
        self._name = name
        self._id = id
        self._icons = icon_urls
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

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
        '_level',
        '_name',
        '_max_level',
        '_village',
    )

    def __init__(self, data, **kwargs):
        self._level = data.get('level')
        self._name = data.get('name')
        self._max_level = data.get('maxLevel')
        self._village = data.get('village')

    @property
    def level(self):
        return self._level

    @property
    def max_level(self):
        return self._max_level

    @property
    def name(self):
        return self._name

    # Return true based on village value
    # @property
    # def is_main_village(self):
    #     return None

"""
achievements": [
    {
      "stars": 0,
      "value": 0,
      "name": {},
      "target": 0,
      "info": {},
      "completionInfo": {},
      "village": "string"
    }
"""

@protected
class Achievement:
    __slots__ = (
        '_name',
        '_stars',
        '_value',
        '_target',
        '_info',
        '_completion_info',
        '_village' # should become an enum
    )

    def __init__(self, data=None, **kwargs):
        self._name = data.get('name', 'Unknown')
        self._stars = data.get('stars', 0)
        self._value = data.get('value', 0)
        self._target = data.get('target', 0)
        self._info = data.get('info', 'Unknown')
        self._completion_info = data.get('completionInfo', 'Unknown')
        self._village = data.get('village', 'Unknown')