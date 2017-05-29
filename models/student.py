

class Student(object):

    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._enrolled_courses = dict()

    @property
    def percentage(self):
        max_marks, obtained_marks = 0, 0
        for course in self._enrolled_courses.values():
            max_marks = course['max_marks']
            obtained_marks = course['obtained_marks']
        return int((obtained_marks * 100) / max_marks) if max_marks else 0

    def full_name(self):
        return "{0}, {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return "<Student - ({0}){1}>".format(self.id, self.first_name)

    def __cmp__(self, other):
        return cmp(other.percentage, self.percentage)
