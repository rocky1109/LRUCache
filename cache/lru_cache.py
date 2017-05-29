
import atexit
from datetime import datetime

import decorators

from _base import Cache, Data
from helpers import Persistable, PickleHelper
from logger import log


class LRUCache(Cache):

    def __init__(self, file_path, limit=20, unique_identifier='id'):
        self._file_path = file_path
        self.limit = limit
        self.unique_identifier = unique_identifier

        # Get the stored dataset into cache
        self._data = Persistable.load(file_path, limit, unique_identifier)

        _count = max(self._data.keys()) if len(self._data) > 0 else 0

        # Form the record_count object, so the new objects use this count to assign id's to new object.
        try:
            self._record_count = max([getattr(data.record, unique_identifier) for data in\
                                      PickleHelper.get_objects_from_file(file_path)])
        except:
            self._record_count = 0

        if self._record_count < _count:
            self._record_count = _count

        log.debug("Max Record count: {0}".format(self._record_count))

        # At exit register to store back the dataset into file.
        atexit.register(Persistable.store, _file_path=self._file_path, _data=self.get_current_dataset)

    def get_current_dataset(self):
        return self._data

    @decorators.overflow
    def insert(self, obj):
        log.debug("Inserting data '{0}' into cache".format(obj))
        # Create Data object.
        data = Data()
        # Save the 'obj' to data object.
        data.record = obj
        # Add the created time to data object.
        data.created_at = datetime.now()

        # Get the unique id form the 'obj'
        unique_id = getattr(obj, self.unique_identifier)
        # Add data object into OrderedDict.
        self._data[unique_id] = data
        log.info("Added '{0}' into cache.".format(obj))

    @decorators.missing
    def retrieve(self, key=None):
        now = datetime.now()

        # If key value is not specified then return all the 'objs' in sorted order.
        # As we are using OrderedDict, which takes care of ordering, hence no need to sort.
        if key is None:
            log.info("Retrieve all datasets available in cache.")
            for data in self._data.values():
                data.accessed += 1
                data.last_accessed = now
            return [data.record for data in self._data.values()]

        log.debug("Retrieve the dataset available with '{0}' = {1}".format(self.unique_identifier, key))
        # Get the value associated to the key passed.
        data = self._data.get(key, None)

        # If associated key isn't present in OrderedDict, then return None
        if data is None:
            log.error("No dataset associated with '{0}' = {1} was found in cache.".format(self.unique_identifier, key))
            return None

        # Increment the 'access' count and 'last_accessed' time attached to data object.
        data.accessed += 1
        data.last_accessed = now

        # To maintain the order as per LRU, remove the data object and re-add it.
        # This will retain the policy.
        del self._data[data.record.id]
        self._data[data.record.id] = data

        log.info("Retrieving dataset '{0}', having '{1}' = {2}".format(data.record, self.unique_identifier, key))

        return data.record

    def _validate(self, key):
        # If key is None, then raise the ValueError
        if not key:
            raise ValueError("Key is required to update the record.")

        # If record is not found as per the key, raise the ValueError
        data = self._data.get(key)
        if data is None:
            raise ValueError("No record found with the given key value '{0}'.".format(key))

        return data

    def update(self, key, obj):
        # Fetch the record from the key.
        old_data = self._validate(key)

        # As updating the data is equivalent to accessing the data.
        # Hence as per the LRU policy to maintain the order, remove and re-add the data object.
        # Also at the same time, update the 'last_modified' time in data object.
        del self._data[key]

        # Assign new 'obj'/record to data object, and change accessibility flags.
        now = datetime.now()
        for attribute in obj.__dict__:
            attr_val = getattr(obj, attribute)
            if attribute != self.unique_identifier and attr_val is not None:
                setattr(old_data.record, attribute, attr_val)

        old_data.last_modified = now
        old_data.last_accessed = now
        old_data.accessed += 1

        # Get the 'unique_identifier' of the 'obj'/record.
        unique_id = getattr(obj, self.unique_identifier)

        # To maintain the order as per the LRU policy add the add back to OrderedDict.
        self._data[unique_id] = old_data

        log.info("Updated dataset '{0}', with '{1}' = {2}".format(old_data.record, self.unique_identifier, key))

    @decorators.underflow
    def remove(self, key):
        # Validate whether the key exists in data list.
        self._validate(key)
        del self._data[key]
        log.info("Deleted dataset with '{0}' = {1}".format(self.unique_identifier, key))
