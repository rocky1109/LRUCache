

class Course(object):

    def __init__(self, id, name, tenure, max_marks):
        self.id = id
        self.name = name
        self.tenure = tenure
        self.max_marks = max_marks

    def __repr__(self):
        return "<Course: ({0}){1}>".format(self.id, self.name)
