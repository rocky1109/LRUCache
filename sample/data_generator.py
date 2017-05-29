
import random
import json


DEST = 'data.json'
MAX_STUDENT_RECORDS = 25
MAX_COURSE_RECORDS = 10

student = {
    "first_name": "Student{0}",
    "last_name": "Something{0}",
    "email": "student{0}@college"
}

RAND_TENURES = [6, 8, 12]
RAND_MAX_MARKS = [50, 60, 70, 80, 90, 100]

course = {
    "name": "course{0}",
    "tenure": 12,
    "max_marks": 100
}


def main():
    students = list()
    courses = list()
    for count in range(1, MAX_STUDENT_RECORDS+1):
        _ = student.copy()
        _["first_name"] = _["first_name"].format(count)
        _["last_name"]  = _["last_name"].format(count)
        _["email"]      = _["email"].format(count)
        students.append(_)

    for count in range(1, MAX_COURSE_RECORDS+1):
        _ = course.copy()
        _["name"]      = _["name"].format(count)
        _["tenure"]    = RAND_TENURES[random.randint(0, len(RAND_TENURES)-1)]
        _["max_marks"] = RAND_MAX_MARKS[random.randint(0, len(RAND_MAX_MARKS)-1)]
        courses.append(_)

    with open(DEST, "w+") as fh:
        json.dump({"students": students, "courses": courses}, fh, indent=4)


if __name__ == "__main__":
    main()
