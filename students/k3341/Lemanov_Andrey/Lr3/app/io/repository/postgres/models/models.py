from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    assignments = relationship('Assignment', back_populates='teacher')


class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)

    teacher = relationship('Teacher', back_populates='assignments', lazy="subquery")
    grading_criteria = relationship('GradingCriteria', back_populates='assignment', lazy="subquery")
    submissions = relationship('Submission', back_populates='assignment', lazy="subquery")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    submissions = relationship('Submission', back_populates='student', lazy="subquery")
    grades = relationship('Grade', back_populates='student', lazy="subquery")


class GradingCriteria(Base):
    __tablename__ = 'grading_criteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    criterion_name = Column(String, nullable=False)
    max_points = Column(Float, nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)

    assignment = relationship('Assignment', back_populates='grading_criteria', lazy="subquery")


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)

    student = relationship('Student', back_populates='submissions', lazy="subquery")
    assignment = relationship('Assignment', back_populates='submissions', lazy="subquery")
    grades = relationship('Grade', back_populates='submission', lazy="subquery")


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    criteria_id = Column(Integer, ForeignKey('grading_criteria.id'), nullable=False)

    student = relationship('Student', back_populates='grades', lazy="subquery")
    submission = relationship('Submission', back_populates='grades', lazy="subquery")
    criteria = relationship('GradingCriteria', lazy="subquery")
