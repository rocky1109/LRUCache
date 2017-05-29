
from cache import Cache
from models import Course


class Courses(Cache):

    def __init__(self):
        self.record_count = 0
        self._courses = dict()

    def insert(self, name, tenure=6, max_marks=100):
        self.record_count += 1
        self._courses[self.record_count] = Course(self.record_count, name, tenure, max_marks)

    def retrieve(self, key=None):
        if key is None:
            return self._courses.values()
        return self._courses[key]

    def update(self, key, name=None, tenure=None, max_marks=None):
        if name == tenure == max_marks is None:
            raise ValueError("Atleast one value should be specified to update the record.")
        old_course = self.retrieve(key=key)
        if name is not None:
            old_course.name = name
        if tenure is not None:
            old_course.tenure = tenure
        if max_marks is not None:
            old_course.max_marks = max_marks

    def remove(self, key):
        del self._courses[key]
