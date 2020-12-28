
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
def build_list(data:Iterable, cls, func=None,**kwargs):
    """Builds a list based on the list provided"""
    if func is not None:
        return [func(cls, instance) for instance in data]
    else:
        return [cls(instance, **kwargs) for instance in data]

def correct_tag(tag:str):
    tag = tag.strip(' ').upper()
    return f'#{tag}' if not tag.startswith('#') else tag

CLASHDATEFORMAT = '%Y%m%dT%H%M%S.000Z'
def format_time(t:str):
    dt = datetime.datetime.strptime(t, CLASHDATEFORMAT)
    return dt

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