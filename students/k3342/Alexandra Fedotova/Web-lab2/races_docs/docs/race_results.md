# Страница с результатами конкретной гонки

Данная страница открывается при переходе со страницы со списком гонок, в случае, если пользователь хочет увидеть результат прошедшей гонки. В результате можно увидеть топ команд, занявших 1-3 место.

## Модель результатов гонки

В модели представлены элементы результатов - команда, позиция и гонка с сортировкой по позиции.

```python
class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  

    class Meta:
        unique_together = ('race', 'team')  
        ordering = ['position']  

    def __str__(self):
        return f"{self.team.name} - Позиция {self.position} в гонке {self.race.date}"
```
## Представление результатов гонки
```python
def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    race_results = RaceResult.objects.filter(race=race).select_related('team')  

    context = {
        'race': race,
        'race_results': race_results,
    }
    return render(request, 'race_results.html', context)
```
## HTML-страница результатов гонки
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Результаты гонки {{ race.date }}</title>
    <style>
        body {
            background-color: #333;
            font-family: Arial, sans-serif;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: radial-gradient(circle, #333 20%, #222 80%);
        }

        .dashboard-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            width: 90%;
            max-width: 1200px;
        }

        .card {
            background-color: #222;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
            border: 2px solid #e10600;
            text-align: center;
        }

        .card h3 {
            color: #e10600;
            margin: 15px 0;
            font-size: 1.5em;
            text-transform: uppercase;
        }

        .card-content {
            margin-top: 10px;
        }

        .table-row {
            background-color: #333;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #444;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .table-row a {
            color: #e10600;
            text-decoration: none;
            font-weight: bold;
        }

        .table-row a:hover {
            color: #ff1e00;
        }

        .no-results {
            color: #e10600;
            font-weight: bold;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <div class="card">
            <h3>Результаты гонки на {{ race.date }}</h3>
            <h4>Время старта: {{ race.start_time }}</h4>
            <div class="card-content">
                {% if race_results %}
                    <div>
                        {% for result in race_results %}
                            <div class="table-row">
                                <span>{{ result.team.name }}</span>
                                <span>Позиция: {{ result.position }}</span>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <p class="no-results">Нет результатов для этой гонки.</p>
                {% endif %}
            </div>
        </div>

        <a href="{% url 'all_races' %}" style="color: #e10600; text-decoration: underline;">Назад к всем гонкам</a>
    </div>

</body>
</html>
```