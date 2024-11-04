# Страница комментариев пользователя 

На этой странице пользователь может увидеть все комментарии, оставленные к гонке, включая собственный. 

## Модель комментария
При добавлении комментариев сохраняются даты заезда, текст комментария, тип комментария (вопрос о сотрудничестве, вопрос о гонках, иное), рейтинг (1-10), информация о комментаторе.
```python
class Comment(models.Model):
    COMMENT_TYPE_CHOICES = [
        ('cooperation', 'Вопрос о сотрудничестве'),
        ('race', 'Вопрос о гонках'),
        ('other', 'Иное')
    ]
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    comment_type = models.CharField(max_length=50, choices=COMMENT_TYPE_CHOICES)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user} к гонке {self.race} ({self.get_comment_type_display()})"
```

## Представление комментариев

**add_comment**: Позволяет пользователю добавлять комментарии к конкретной гонке. Если запрос поступает методом POST, функция проверяет корректность данных из формы. В случае успеха она создает новый комментарий, связывает его с гонкой и текущим пользователем, после чего сохраняет его и перенаправляет на страницу комментариев гонки. Если запрос не POST, отображается пустая форма для добавления комментария.

**race_comments**: Отображает все комментарии, связанные с конкретной гонкой. 
```python
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.user = request.user
            comment.save()
            return redirect('race_comments', race_id=race.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'race': race})


@login_required
def race_comments(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments = Comment.objects.filter(race=race)
    return render(request, 'race_comments.html', {'race': race, 'comments': comments})
```

## HTML-страница комментариев к гонке
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Комментарии к гонке</title>
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

        .race-item {
            background-color: #333;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #444;
        }

        .race-item p {
            margin: 5px 0;
        }

        .race-item strong {
            color: #e10600;
        }

        .race-item a {
            color: #e10600;
            text-decoration: none;
            font-weight: bold;
        }

        .race-item a:hover {
            color: #ff1e00;
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        <div class="card">
            <h3>Комментарии к гонке</h3>
            <div class="card-content">
                <p>Дата гонки: {{ race.date }} {{ race.start_time }}</p>
                {% if comments %}
                    <ul>
                        {% for comment in comments %}
                            <li class="race-item">
                                <p><strong>Комментатор:</strong> {{ comment.user.username }}</p>
                                <p><strong>Тип комментария:</strong> {{ comment.get_comment_type_display }}</p>
                                <p><strong>Рейтинг:</strong> {{ comment.rating }}</p>
                                <p><strong>Комментарий:</strong> {{ comment.text }}</p>
                                <p><strong>Дата добавления:</strong> {{ comment.date_created }}</p>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>Комментариев пока нет.</p>
                {% endif %}
                <a href="{% url 'add_comment' race.id %}">Добавить комментарий</a>
            </div>
        </div>
    </div>

</body>
</html>
```