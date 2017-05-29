
from cache.lru_cache import LRUCache

from models import Student
from courses import Courses

from logger import log


class Students(LRUCache):

    def __init__(self, *args, **kwargs):
        super(Students, self).__init__(*args, **kwargs)
        self.courses = Courses()

    def insert(self, first_name, last_name, email):
        self._record_count += 1
        student = Student(self._record_count, first_name, last_name, email)
        super(Students, self).insert(student)

    def update(self, id, first_name=None, last_name=None, email=None):
        if first_name == last_name == email is None:
            raise ValueError('No new value was found to update.')
        student = self.retrieve(key=id)
        if first_name is not None:
            student.first_name = first_name
        if last_name is not None:
            student.last_name = last_name
        if email is not None:
            student.email = email
        super(Students, self).update(id, student)

    def enroll_to_course(self, student_id, course_id):
        student = self.retrieve(key=student_id)
        course = self.courses.retrieve(key=course_id)
        log.info("** Enrolling '{0}' to '{1}' **".format(student, course))
        if not student._enrolled_courses.has_key(course_id):
            student._enrolled_courses[course_id] = {'max_marks': course.max_marks, 'obtained_marks': 0}
            super(Students, self).update(student_id, student)

    def disenroll_from_course(self, student_id, course_id):
        student = self.retrieve(key=student_id)
        log.info("** Disenrolling '{0}' from Course id. '{1}' **".format(student, course_id))
        if not student._enrolled_courses.has_key(course_id):
            try:
                del student._enrolled_courses[course_id]
            except:
                pass
        super(Students, self).update(student_id, student)

    def set_marks(self, student_id, course_id, marks):
        student = self.retrieve(key=student_id)
        log.info("** Setting marks for '{0}' in Course id. '{1}' [marks={2}] **".format(student, course_id, marks))
        if student._enrolled_courses.has_key(course_id):
            student._enrolled_courses[course_id]['obtained_marks'] = marks
            super(Students, self).update(student_id, student)
        else:
            raise ValueError("'{0}' is not enrolled to '{1}'.".format(student, self.courses.retrieve(key=course_id)))
