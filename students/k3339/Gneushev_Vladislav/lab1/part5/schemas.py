from dataclasses import dataclass


@dataclass
class CreateDisciplineScore:
    discipline: str
    grade: int
