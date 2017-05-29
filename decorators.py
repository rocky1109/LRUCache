
from collections import OrderedDict
from datetime import datetime

from helpers import PickleHelper
from logger import log


def overflow(function):
    def func(self, *args, **kwargs):
        header = "*  Cache - {0} operation  *".format(function.__name__)
        log.debug('*' * len(header))
        log.debug(header)
        log.debug('*' * len(header))
        # Check the cache size and data available in system.
        # If its reached the max. limit, then add least recently used data into file.
        if self.limit <= len(self._data):
            log.debug("  Cache was overflown.")
            # As per the OrderedDict the first data is least recently used data.
            lru_id = self._data.keys()[0]
            lru_object = self._data[lru_id]
            # Remove the least recently used data from list and add it into file
            del self._data[lru_id]
            PickleHelper.add_object_to_file(self._file_path, lru_object)
            log.debug("  Storing '{0}' to file to empty the cache.".format(lru_object))
        return function(self, *args, **kwargs)
    return func


def underflow(function):
    def func(self, *args, **kwargs):
        header = "*  Cache - {0} operation  *".format(function.__name__)
        log.debug('*' * len(header))
        log.debug(header)
        log.debug('*' * len(header))

        try:
            function(self, *args, **kwargs)
            proceed = False
        except ValueError:
            proceed = True
        except Exception:
            raise ValueError("Key was found not in data list.")

        # Get the key from the parameter
        if kwargs.has_key('key'):
            key = kwargs.get('key')
        elif len(args) >= 1:
            key = args[0]
        else:
            key = None

        if proceed:
            if key is not None:
                log.debug("  Dataset with '{0}' = {1} was not found in data list, "
                          "hence removing it from file if present.".format(self.unique_identifier, key))
                deleted = PickleHelper.remove_object_from_file(self._file_path, self.unique_identifier, key)
                if deleted:
                    log.info("  Deleted dataset from file.")
                else:
                    log.error("  Record was not found in file, delete fail.")
        else:
            log.debug("  Removed the dataset with '{0}' = {1} from data list.".format(self.unique_identifier, key))
            stored_data = PickleHelper.get_objects_from_file(self._file_path)
            if len(stored_data) > 0:
                data = stored_data[0]
                log.debug("  Readjusting the cache, moving '{0}' from file.".format(data))
                
                uid = getattr(data.record, self.unique_identifier)
                PickleHelper.remove_object_from_file(self._file_path, self.unique_identifier, uid)
    
                _data_copy = self._data
                self._data = OrderedDict()
    
                self._data[uid] = data
    
                for uid, data in _data_copy.items():
                    self._data[uid] = data
            else:
                log.debug("  No elements in file stored to readjust the cache.")

    return func


def missing(function):

    def func(self, *args, **kwargs):
        header = "*  Cache - {0} operation  *".format(function.__name__)
        log.debug('*' * len(header))
        log.debug(header)
        log.debug('*' * len(header))

        ret = function(self, *args, **kwargs)

        # If the return value is None, means 'obj'/record was not found in data list.
        # As data may be present in file, hence we need to check its presence in file.
        if ret is None:

            # Get the key from the parameter
            if kwargs.has_key('key'):
                key = kwargs.get('key')
            elif len(args) >= 1:
                key = args[0]
            else:
                key = None

            # If a valid key paramter found then scan the records from the file.
            if key is not None:
                log.debug("  Dataset with '{0}' = {1} was not found in cache, looking into file.".\
                          format(self.unique_identifier, key))
                # Fetch the records from the file.
                datas = PickleHelper.get_objects_from_file(self._file_path)

                # Check whether the 'obj'/record is present with the target identifier value.
                for data in datas:
                    unique_id = getattr(data.record, self.unique_identifier)
                    # If found, then change accessibility flag values.
                    if unique_id == key:
                        ret = data
                        data.accessed += 1
                        data.last_accessed = datetime.now()

                        log.debug("  Data '{0}' with '{1}' = {2} was found in file.".\
                                  format(data,self.unique_identifier, unique_id))
                        break

                # If valid record was found, then as per the LRU policy check the accessibility matrix, and,
                # if the returning 'obj'/record has more 'accessed' value than any data in list then,
                # swap the record among file and data list.
                if ret is not None:
                    # Find the least accessed data from the data list.
                    least_accessed_data = min([data.accessed for data in self._data.values()])
                    # If least accessed data from list is less than returning object then swap it.
                    if least_accessed_data <= ret.accessed:
                        readjustment = False
                        log.debug("  Looking for readjustment of data in cache and file.")
                        for data in self._data.values():
                            if data.accessed == least_accessed_data:
                                # Get the least accessed data from the list, and remove it.
                                unique_id = getattr(data.record, self.unique_identifier)
                                lru_object = self._data[unique_id]
                                del self._data[unique_id]

                                # Add the returning object into data list.
                                unique_id = getattr(ret.record, self.unique_identifier)
                                self._data[unique_id] = ret

                                # Add the least accessed data back to file.
                                PickleHelper.remove_object_from_file(self._file_path, self.unique_identifier, unique_id)

                                ret = ret.record
                                log.debug("  Swapping data from file '{0}' to cache, at place of '{1}'.".format(ret, lru_object))
                                readjustment = True

                                PickleHelper.add_object_to_file(self._file_path, lru_object)
                                break
                        if not readjustment:
                            log.debug("  No candidate found for readjustment.")
                    else:
                        log.debug("  Retrieving data doesn't qualify for readjustments into cache.")
                else:
                    log.error("  Dataset with '{0}' = {1} was not found in file.".format(self.unique_identifier, key))
        return ret

    return func
