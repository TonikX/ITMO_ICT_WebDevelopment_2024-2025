import asyncio

from sqlalchemy import select

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import AsyncSessionLocal, get_db
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models.models import *


async def add_data(db_session: AsyncSessionLocal):
    # Create a new session
    async with db_session as session:
        async with session.begin():  # Begin a transaction
            # Create a teacher
            teacher1 = Teacher(name="Dr. Smith", surname="Smith")
            session.add(teacher1)

            # Create some assignments
            assignment1 = Assignment(title="Math Homework 1", description="Solve all the problems", teacher=teacher1)
            assignment2 = Assignment(title="Science Project", description="Complete the science experiment",
                                     teacher=teacher1)
            session.add(assignment1)
            session.add(assignment2)

            # Add grading criteria
            criteria1 = GradingCriteria(criterion_name="Accuracy", max_points=10, assignment=assignment1)
            criteria2 = GradingCriteria(criterion_name="Creativity", max_points=10, assignment=assignment2)
            session.add(criteria1)
            session.add(criteria2)

            # Create students
            student1 = Student(name="John Doe", surname="Smith")
            student2 = Student(name="Jane Doe", surname="Smith")
            session.add(student1)
            session.add(student2)

            # Create submissions
            submission1 = Submission(content="My Math Homework", student=student1, assignment=assignment1)
            submission2 = Submission(content="My Math Homework", student=student2, assignment=assignment1)
            submission3 = Submission(content="My Science Project", student=student1, assignment=assignment2)
            submission4 = Submission(content="My Science Project", student=student2, assignment=assignment2)
            session.add(submission1)
            session.add(submission2)
            session.add(submission3)
            session.add(submission4)

            # Add grades
            grade1 = Grade(grade=9.5, student=student1, submission=submission1, criteria=criteria1)
            grade2 = Grade(grade=8.0, student=student2, submission=submission2, criteria=criteria1)
            grade3 = Grade(grade=9.0, student=student1, submission=submission3, criteria=criteria2)
            grade4 = Grade(grade=9.5, student=student2, submission=submission4, criteria=criteria2)
            session.add(grade1)
            session.add(grade2)
            session.add(grade3)
            session.add(grade4)

        # Commit the session
        await session.commit()


# Asynchronous function to query data and verify insertion

async def query_data(db_session: AsyncSessionLocal):
    async with db_session as session:
        result = await session.execute(select(Teacher))
        teachers = result.scalars().all()
        for teacher in teachers:
            print(teacher.name)


# Run the asynchronous functions
async def main():
    db_session = await get_db()
    # Create all tables

    # Add data
    await add_data(db_session)

    # Query and display the data
    await query_data(db_session)


# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
