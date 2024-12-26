import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON;')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    is_specialized BOOLEAN DEFAULT 0
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    is_specialized BOOLEAN DEFAULT 0
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    has_own_classroom BOOLEAN DEFAULT 0,
    classroom_id INTEGER,
    FOREIGN KEY (classroom_id) REFERENCES Classrooms(id) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Teachers_Subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    subject_id INTEGER,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('M', 'F')),
    start_date DATE,
    end_date DATE,
    class_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    class_teacher_id INTEGER,
    FOREIGN KEY (class_teacher_id) REFERENCES Teachers(id) ON DELETE SET NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day_of_week TEXT CHECK(day_of_week IN ('MON', 'TUE', 'WED', 'THU', 'FRI')),
    lesson_number INTEGER NOT NULL,
    class_id INTEGER,
    subject_id INTEGER,
    teacher_id INTEGER,
    classroom_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES Classes(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    FOREIGN KEY (classroom_id) REFERENCES Classrooms(id),
    UNIQUE (class_id, day_of_week, lesson_number)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER CHECK (grade BETWEEN 2 AND 5),
    quarter INTEGER CHECK (quarter BETWEEN 1 AND 4),
    year INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id),
    UNIQUE (student_id, subject_id, quarter, year)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS GradeHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    old_grade INTEGER,
    new_grade INTEGER,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quarter INTEGER,
    year INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ClassTeachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER,
    class_id INTEGER,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (teacher_id) REFERENCES Teachers(id),
    FOREIGN KEY (class_id) REFERENCES Classes(id),
    UNIQUE (teacher_id, class_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER,
    lesson_date DATE,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late', 'Excused')) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes(id) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS DisciplinaryRecords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    violation_description TEXT,
    violation_date DATE,
    punishment TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT,
    email TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS StudentParents (
    student_id INTEGER,
    parent_id INTEGER,
    relationship TEXT CHECK(relationship IN ('Mother', 'Father', 'Guardian')) NOT NULL,
    PRIMARY KEY (student_id, parent_id),
    FOREIGN KEY (student_id) REFERENCES Students(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES Parents(id) ON DELETE CASCADE
);
''')

conn.commit()
conn.close()
