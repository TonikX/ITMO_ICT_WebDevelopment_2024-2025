from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()


@app.get("/")
def read_index():
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
