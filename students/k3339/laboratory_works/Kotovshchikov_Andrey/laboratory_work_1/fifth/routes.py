import time
from request import Request
from response import Response

from repository import InMemorySubjectRepository
from service import SubjectService
from subject import Subject

subject_service = SubjectService(repository=InMemorySubjectRepository())


def get_all_subjects(request: Request, student_id: int):
    subjects = subject_service.get_all_student_subjects(student_id)
    accept = request.headers.get("Accept")
    if "text/html" not in accept:
        return Response(status_code=406, reason="Not Acceptable")

    body = "<html><head></head><body>"
    body += f"<div>Дисциплины студента ({len(subjects)})</div>"
    body += "<ul>"
    for subject in subjects:
        body += "<li>"
        body += f"<div>#{subject.id}</div>"
        body += f"<div>Название: {subject.name}</div>"
        body += f"<div>Описание: {subject.description}</div>"
        body += f"<div>Оценка: {subject.assessment}</div>"
        body += "</li>"

    body += "</ul>"
    body += "</body></html>"
    body = body.encode()

    response = Response(status_code=200, reason="OK", body=body)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["Content-Length"] = len(body)
    return response


def save_subject(request: Request, student_id: int):
    subject = Subject(
        student_id=student_id,
        name=request.query["name"][0],
        description=request.query["description"][0],
        assessment=request.query["assessment"][0],
    )

    subject_service.save(subject)
    return Response(status_code=201, reason="CREATED")
