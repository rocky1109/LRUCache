
import os
import cPickle
from collections import OrderedDict

from logger import log


class PickleHelper(object):

    @staticmethod
    def add_newly_objects_to_file(file_path, objects):
        with open(file_path, 'wb+') as fh:
            cPickle.dump(objects, fh) #, cPickle.HIGHEST_PROTOCOL)

    @staticmethod
    def add_object_to_file(file_path, obj):
        try:
            with open(file_path, 'rb') as fh:
                li = cPickle.load(fh)
        except Exception as err:
            li = list()

        li.append(obj)
        li.sort(cmp=lambda x, y: cmp(x.record, y.record))

        with open(file_path, 'wb+') as fh:
            cPickle.dump(li, fh) #, cPickle.HIGHEST_PROTOCOL)

    @staticmethod
    def get_objects_from_file(file_path):
        try:
            with open(file_path, 'rb') as fh:
                _ = cPickle.load(fh)
                _.sort(cmp=lambda x, y: cmp(x.record, y.record))
        except Exception as err:
            _ = list()
        return _

    @staticmethod
    def remove_object_from_file(file_path, unique_identifier, id):
        success = False
        try:
            li = PickleHelper.get_objects_from_file(file_path)
        except Exception as err:
            return success
        count = 0
        found = False
        for item in li:
            uid = getattr(item.record, unique_identifier)
            if uid == id:
                found = True
                break
            count += 1
        if found:
            li.pop(count)
            success = True
        with open(file_path, 'wb+') as fh:
            cPickle.dump(li, fh)#, cPickle.HIGHEST_PROTOCOL)
        return success


class Persistable(object):

    @staticmethod
    def store(_file_path, _data):
        header = "*  Persistance class - Store  *"
        log.debug('*' * len(header))
        log.debug(header)
        log.debug('*' * len(header))

        # Fetching the current dataset of cache.
        _data = _data()
        cache_data = _data.values()

        # Get the dataset from file.
        stored_data = PickleHelper.get_objects_from_file(_file_path)

        log.debug("  Collecting stored data from file: '{0}'".format(os.path.basename(_file_path)))
        log.debug("  Stored data in file: {0}".format(stored_data))
        log.debug("  Current Cache contents: {0}".format(cache_data))

        # Extend the stored dataset with cache dataset, and sort it before storing back to file.
        stored_data.extend(cache_data)
        log.debug("  Extending the fetched data sets and sorting to store it back.")
        stored_data.sort(cmp=lambda x, y: cmp(x.record, y.record))

        PickleHelper.add_newly_objects_to_file(_file_path, stored_data)
        log.info("Stored {0} cache datasets back to file '{1}'."\
                 .format(len(_data), os.path.basename(_file_path)))

    @staticmethod
    def load(_file_path, limit, unique_identifier):
        header = "*  Persistance class - Load  *"
        log.debug('*' * len(header))
        log.debug(header)
        log.debug('*' * len(header))

        log.debug("  Fetching dataset from file: '{0}'".format(_file_path))
        # Fetch the stored datasets.
        stored_data = PickleHelper.get_objects_from_file(_file_path)

        log.debug("  Cache Limit: {0}".format(limit))
        log.debug("  Unique Identifier attribute: {0}".format(unique_identifier))

        # Get the datasets of size of cache limit and sort it for cache.
        # While rest of the dataset should be stored back into file.
        count = 0
        _data = OrderedDict()

        stored_data.sort(cmp=lambda x, y: cmp(x.record, y.record))
        for dataset in stored_data:
            if count >= limit:
                break
            uid = getattr(dataset.record, unique_identifier)
            _data[uid] = dataset
            PickleHelper.remove_object_from_file(_file_path, unique_identifier, uid)
            count += 1

        log.debug("  Complete dataset: {0}".format(stored_data))
        log.debug("  Returning dataset: {0}".format(_data))
        log.info("Loaded {0} datasets into cache from file: '{1}'"\
                 .format(len(_data), os.path.basename(_file_path)))
        return _data
