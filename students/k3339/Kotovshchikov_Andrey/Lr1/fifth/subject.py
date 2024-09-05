from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True, slots=True)
class Subject:
    id: UUID = field(init=False, default_factory=uuid4)
    student_id: int
    name: str
    description: str
    assessment: int
