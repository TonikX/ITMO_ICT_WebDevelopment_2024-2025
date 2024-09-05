from typing import Iterable
from repository import SubjectRepositoty
from subject import Subject


class SubjectService:
    _repository: SubjectRepositoty

    def __init__(self, repository: SubjectRepositoty) -> None:
        self._repository = repository

    def get_all_student_subjects(self, student_id: int) -> Iterable[Subject]:
        return self._repository.get_by_student_id(student_id)

    def save(self, subject: Subject) -> None:
        self._repository.save(subject)
