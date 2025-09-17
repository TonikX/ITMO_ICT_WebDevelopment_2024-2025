from celery_config import app
from parse_functions import parse_and_save

@app.task
def parse_url_task(url: str, tag_name: str):
    return parse_and_save(url, tag_name)