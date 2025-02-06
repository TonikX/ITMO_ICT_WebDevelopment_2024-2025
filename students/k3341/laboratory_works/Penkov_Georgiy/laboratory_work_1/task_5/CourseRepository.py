from Course import Course


class CourseRepository:
    def __init__(self):
        self.courses: list[Course] = []

    def get_courses(self) -> list[Course]:
        return self.courses

    def insert_course(self, name: str, grade: int):
        id = len(self.courses) + 1
        if grade < 0:
            raise Exception("Grade must not be negative.")
        course = Course(id, name, grade)
        self.courses.append(course)
