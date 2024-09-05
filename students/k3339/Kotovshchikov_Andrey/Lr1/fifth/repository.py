from typing import Iterable, Protocol
from uuid import UUID

from subject import Subject


class SubjectRepositoty(Protocol):
    def get_by_student_id(self, student_id: int) -> Iterable[Subject]: ...

    def save(self, subject: Subject) -> None: ...


class InMemorySubjectRepository(SubjectRepositoty):
    _subjects: dict[UUID, Subject]

    def __init__(self) -> None:
        self._subjects = dict()

    def get_by_student_id(self, student_id: int) -> Iterable[Subject]:
        student_subjects = []
        for subject in self._subjects.values():
            if subject.student_id == student_id:
                student_subjects.append(subject)

        return student_subjects

    def save(self, subject: Subject) -> None:
        self._subjects[subject.id] = subject
