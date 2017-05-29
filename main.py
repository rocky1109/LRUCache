
import json

import settings

from views import Students


def get_sample_data(sample_json_file):
    with open(sample_json_file) as fh:
        return json.load(fh)


def main():

    sample_data = get_sample_data(settings.SAMPLE_DATA)

    cache = Students(file_path=settings.CACHE_FILE_PATH, limit=settings.CACHE_LIMIT)

    for student in sample_data['students']:
        cache.insert(**student)

    #print cache._data
    cache.retrieve(key=2)
    #print cache._data
    cache.remove(key=3)
    #print cache._data
    cache.remove(key=4)
    #print cache._data

    for course in sample_data['courses']:
        cache.courses.insert(**course)

    cache.enroll_to_course(1, 1)
    cache.enroll_to_course(2, 2)
    cache.set_marks(1, 1, 50)
    cache.set_marks(2, 2, 40)
    cache.disenroll_from_course(2, 2)


if __name__ == '__main__':
    main()
