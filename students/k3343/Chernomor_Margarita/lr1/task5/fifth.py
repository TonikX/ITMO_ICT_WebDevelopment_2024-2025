from urllib.parse import unquote
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

grades = {}


@app.get("/")
def read_grades():
    content = "<h1>Оценки по дисциплинам</h1><ul>"
    for subject, grade in grades.items():
        content += f"<li>{subject}: {grade}</li>"
    content += "</ul>"
    return HTMLResponse(content=content)


@app.post("/submit/")
def submit_grade(subject: str = Form(...), grade: int = Form(...)):
    subject = unquote(subject)
    grades[subject] = grade
    return {"message": "Оценка добавлена"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
