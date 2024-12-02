import sqlite3


def insert_classrooms():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    classrooms = [
        ('101', True),
        ('102', False),
        ('103', False),
        ('104', True),
        ('105', False),
    ]

    cursor.executemany('''
        INSERT INTO Classrooms (number, is_specialized)
        VALUES (?, ?)
    ''', classrooms)

    conn.commit()
    conn.close()


insert_classrooms()


def insert_subjects():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    subjects = [
        ('Mathematics', False),
        ('Physics', True),
        ('Chemistry', False),
        ('Informatics', True),
        ('English', False),
    ]

    cursor.executemany('''
        INSERT INTO Subjects (name, is_specialized)
        VALUES (?, ?)
    ''', subjects)

    conn.commit()
    conn.close()


insert_subjects()


def insert_teachers():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    teachers = [
        ('John', 'Doe', True, 1),  # John преподает в кабинете 101
        ('Jane', 'Smith', False, 2),  # Jane преподает в кабинете 102
        ('Tom', 'Brown', True, 3),  # Tom преподает в кабинете 103
        ('Alice', 'Davis', False, 4),  # Alice преподает в кабинете 104
        ('Bob', 'White', False, 5),  # Bob преподает в кабинете 105
    ]

    cursor.executemany('''
        INSERT INTO Teachers (first_name, last_name, has_own_classroom, classroom_id)
        VALUES (?, ?, ?, ?)
    ''', teachers)

    conn.commit()
    conn.close()


insert_teachers()


def insert_classes():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    classes = [
        ('10A', '2023-09-01', None, 1),  # Класс 10A, классный руководитель John Doe
        ('10B', '2023-09-01', None, 2),  # Класс 10B, классный руководитель Jane Smith
    ]

    cursor.executemany('''
        INSERT INTO Classes (name, start_date, end_date, class_teacher_id)
        VALUES (?, ?, ?, ?)
    ''', classes)

    conn.commit()
    conn.close()


insert_classes()


def insert_schedules():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    schedules = [
        (1, 'MON', 1, 1, 1, 1),  # 10A, Понед, 1 урок, Информатика, учитель John Doe, кабинет 101
        (1, 'MON', 2, 2, 2, 2),  # 10A, Понед, 2 урок, Математика, учитель Jane Smith, кабинет 102
        (2, 'MON', 1, 3, 3, 3),  # 10B, Понед, 1 урок, Физика, учитель Tom Brown, кабинет 103
        (2, 'MON', 2, 4, 4, 4),  # 10B, Понед, 2 урок, Химия, учитель Alice Davis, кабинет 104
    ]

    cursor.executemany('''
        INSERT INTO Schedules (class_id, day_of_week, lesson_number, subject_id, teacher_id, classroom_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', schedules)

    conn.commit()
    conn.close()


insert_schedules()


def insert_students():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    students = [
        ('John', 'Johnson', 'M', '2023-09-01', None, 1),  # Студент 1, класс 10A
        ('Emma', 'Williams', 'F', '2023-09-01', None, 1),  # Студентка 2, класс 10A
        ('Sophia', 'Taylor', 'F', '2023-09-01', None, 2),  # Студентка 3, класс 10B
        ('Lucas', 'Moore', 'M', '2023-09-01', None, 2),  # Студент 4, класс 10B
    ]

    cursor.executemany('''
        INSERT INTO Students (first_name, last_name, gender, start_date, end_date, class_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', students)

    conn.commit()
    conn.close()


insert_students()


def insert_grades():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    grades = [
        (1, 1, 5, 1, 2023),  # Оценка студента 1 по предмету Информатика, 5 баллов, 1 квартал 2023 года
        (1, 2, 4, 1, 2023),  # Оценка студента 1 по предмету Математика, 4 балла, 1 квартал 2023 года
        (2, 1, 5, 1, 2023),  # Оценка студента 2 по предмету Информатика, 5 баллов, 1 квартал 2023 года
        (2, 3, 4, 1, 2023),  # Оценка студента 2 по предмету Физика, 4 балла, 1 квартал 2023 года
    ]

    cursor.executemany('''
        INSERT INTO Grades (student_id, subject_id, grade, quarter, year)
        VALUES (?, ?, ?, ?, ?)
    ''', grades)

    conn.commit()
    conn.close()


insert_grades()


def get_subject_in_class(class_id, day_of_week, lesson_number):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    query = '''
    SELECT s.name AS subject_name, 
           t.first_name AS teacher_first_name, 
           t.last_name AS teacher_last_name, 
           c.number AS classroom_number
    FROM Schedules sc
    JOIN Subjects s ON sc.subject_id = s.id
    JOIN Teachers t ON sc.teacher_id = t.id
    JOIN Classrooms c ON sc.classroom_id = c.id
    WHERE sc.class_id = ?
      AND sc.day_of_week = ?
      AND sc.lesson_number = ?
    '''
    cursor.execute(query, (class_id, day_of_week, lesson_number))
    result = cursor.fetchall()
    conn.close()

    return result

class_id = 1
day_of_week = 'MON'
lesson_number = 1
subjects = get_subject_in_class(class_id, day_of_week, lesson_number)

for subject in subjects:
    print(subject)

