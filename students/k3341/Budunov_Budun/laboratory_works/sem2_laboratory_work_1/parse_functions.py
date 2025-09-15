import requests
from sqlmodel import Session, select
from models import Tag
from database import engine

def parse_and_save(url, tag_name):
    """
    Парсит веб-страницу и сохраняет заголовки в базу данных.
    
    Args:
        url (str): URL-адрес для парсинга
        tag_name (str): Имя тега для добавления к заголовкам
    
    Returns:
        list: Список заголовков, сохраненных в базе
    """
    try:
        # Получаем данные с URL
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        titles = []
        # Проверяем, является ли ответ JSON-объектом от OpenAlex API
        if 'results' in data and data['results'] is not None:
            for item in data['results']:
                title = f"{item['title']} {tag_name}"
                with Session(engine) as session:
                    existing_tag = session.exec(select(Tag).where(Tag.name == title)).first()
                    if not existing_tag:
                        tag = Tag(name=title)
                        session.add(tag)
                        session.commit()
                        print(f"Сохранен тег: {title}")
                    else:
                        print(f"Тег уже существует: {title}")
                    titles.append(title)
        else:
            print("Заголовки не найдены")
            titles.append("No titles found")
        
        return titles
    
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return [f"Error: {str(e)}"]

def worker(urls, tag_name):
    """
    Обрабатывает список URL для парсинга.
    
    Args:
        urls (list): Список URL-адресов
        tag_name (str): Имя тега
    
    Returns:
        list: Список всех заголовков
    """
    all_titles = []
    for url in urls:
        titles = parse_and_save(url, tag_name)
        all_titles.extend(titles)
    return all_titles