
import datetime

from typing import Union, Iterable
from collections import deque

# search(members, tag="#mytag")
def search(iterable, predicate):
    """Returns members in the iterable that meet the specification of the predicate"""
    return list(filter(predicate, iterable))


def find(iterable, predicate):
    """Returns the first element that satisfies the specified predicate"""

    for i in iterable:
        if predicate(i): return i
    return None


# build_list([{id=5, name="hello"}], cls, lambda cls, : )
def build_list(data:Iterable, cls, func=None, **kwargs):
    """Builds a list based on the list provided"""
    if func is not None:
        return [func(cls, instance) for instance in data]
    else:
        return [cls(instance, **kwargs) for instance in data]


def execute_if_found(data:dict, look:str, func, default=None, **func_kwargs):
    """Call get on the dict passed with an option for a default value and a func to pass the data through"""
    try:
        result = data[look]
        return func(result, **func_kwargs)
    except KeyError: return default
    

def correct_tag(tag:str):
    tag = tag.strip(' ').upper()
    return f'#{tag}' if not tag.startswith('#') else tag


CLASHDATEFORMAT = '%Y%m%dT%H%M%S.000Z'
def format_time(t:str):
    dt = datetime.datetime.strptime(t, CLASHDATEFORMAT)
    return dt


def protected(cls):
    """Protects class instance attributes from being changed after initialization"""

    def new_setattr(self, name, value):
        try: object.__getattribute__(self, name)
        except AttributeError: object.__setattr__(self, name, value)
        else: raise AttributeError(f'Can not set attribute: {name}')

    cls.__setattr__ = new_setattr
    return cls


class LRUCache(dict):
    
    def __init__(self, max):
        self.max_size = max
        self.__keys = deque()
        super().__init__()

    def __maintain_max_size(self):
        while len(self) > self.max_size:
            del self[self.__keys.popleft()]

    def __setitem__(self, key, value):
        self.__keys.append(key)
        super().__setitem__(key, value)
        self.__maintain_max_size()

    def __getitem__(self, key):
        self.__maintain_max_size()
        return super().__getitem__(key)

    def __contains__(self, key):
        self.__maintain_max_size()
        return super().__contains__(key)