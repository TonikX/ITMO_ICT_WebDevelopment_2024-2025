# Страница списка всех гонок

На странице отображены все актуальные гонки с датой и временем заезда. Для прошедших гонок можно нажать кнопку "посмотреть результат" - она перенаправит на страницу с результатом конкретной гонки. Если гонка еще не прошла или нет результата выводится надпись "результата пока нет". 

## Модель гонки
```python
class Race(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Гонка {self.date} в {self.start_time}"
```
## Представление списка всех гонок 

Выводим все гонки в личном кабинете с сортировкой по дате и времени.

```python
def all_races(request):
    races = Race.objects.all().order_by('date', 'start_time')
    print(races) 
    return render(request, 'all_races.html', {'races': races})
```
## HTML-страница списка всех гонок 
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Все гонки</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #333;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        .container {
            max-width: 800px;
            width: 100%;
            padding: 20px;
            background-color: #222;
            border-radius: 8px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
        }

        h1 {
            text-align: center;
            color: #e10600;
        }

        .race-list {
            list-style-type: none;
            padding: 0;
        }

        .race-item {
            background-color: #333;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #444;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .race-item span {
            color: #e10600;
            font-weight: bold;
        }

        .race-item p {
            margin: 0;
        }

        .btn-result {
            background-color: #e10600;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            cursor: pointer;
            text-decoration: none;
        }

        .btn-result:hover {
            background-color: #ff1e00;
        }

        .btn-back {
            display: block; /* Чтобы кнопка занимала всю ширину */
            text-align: center; /* Выравнивание текста по центру */
            margin-top: 20px; /* Отступ сверху */
            padding: 10px;
            background-color: #444; /* Цвет фона */
            color: white; /* Цвет текста */
            border: none; /* Без рамки */
            border-radius: 5px; /* Закругленные углы */
            text-decoration: none; /* Без подчеркивания */
        }

        .btn-back:hover {
            background-color: #666; /* Изменение цвета при наведении */
        }

    </style>
</head>
<body>

<div class="container">
    <h1>Все гонки</h1>
    <ul class="race-list">
        {% for race in races %}
            <li class="race-item">
                <div>
                    <span>Дата:</span> {{ race.date }} <br>
                    <span>Время:</span> {{ race.start_time }}
                </div>
                <div>
                    {% if race.result %}
                        <a href="{% url 'race_results' race.id %}" class="btn-result">Посмотреть результат</a>
                    {% else %}
                        <p>Результат еще не опубликован</p>
                    {% endif %}
                </div>
            </li>
        {% empty %}
            <p>Нет доступных гонок.</p>
        {% endfor %}
        
    </ul>
    <a href="{% url 'participant_dashboard' %}" class="btn-back">Назад в личный кабинет</a>
</div>

</body>
</html>
```