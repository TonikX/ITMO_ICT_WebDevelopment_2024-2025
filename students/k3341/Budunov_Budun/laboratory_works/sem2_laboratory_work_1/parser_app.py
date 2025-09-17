from fastapi import FastAPI
from task_async import task_2 as async_parse
from task_threading import task_2 as threading_parse
from task_multiprocessing import task_2 as multiprocessing_parse

app = FastAPI()

@app.get("/parse/{mode}")
async def run_parser(mode: str = "async", url: str = "https://api.openalex.org/works?per-page=50&page=1"):
    if mode == "async":
        result = await async_parse(url)
        return {"status": "Async parsing completed", "result": result}
    elif mode == "threading":
        result = threading_parse(url)
        return {"status": "Threading parsing completed", "result": result}
    elif mode == "multiprocessing":
        result = multiprocessing_parse(url)
        return {"status": "Multiprocessing parsing completed", "result": result}
    else:
        return {"error": "Invalid mode. Use 'async', 'threading' or 'multiprocessing'"}