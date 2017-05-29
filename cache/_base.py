
import os
import abc
from logger import log

from helpers import PickleHelper
from collections import OrderedDict


class Cache(object):

    @abc.abstractmethod
    def insert(self, obj):
        pass

    @abc.abstractmethod
    def retrieve(self, key=None):
        pass

    @abc.abstractmethod
    def update(self, key, obj):
        pass

    @abc.abstractmethod
    def remove(self, key):
        pass


class Data(object):
    record = None
    last_accessed = None
    accessed = 0
    last_modified = None
    created_at = None

    def __repr__(self):
        return self.record.__repr__()

    def __cmp__(self, other):
        if self.last_accessed is None or other.last_accessed is None:
            return cmp(self.accessed, other.accessed)
        elif self.accessed == other.accessed:
            return cmp(self.last_accessed, other.last_accessed)
        else:
            return cmp(self.created_at, other.created_at)
