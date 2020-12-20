
# Later will house utilities to parse the recieved data into classes
# and will also house the request method
from collections import deque

def correct_tag(tag:str):
    tag = tag.strip(' ').upper()
    return f'#{tag}' if not tag.startswith('#') else tag

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