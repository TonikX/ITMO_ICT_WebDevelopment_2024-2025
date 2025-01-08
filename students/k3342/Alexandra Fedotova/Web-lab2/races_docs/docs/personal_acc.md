# Страница личного кабинета участника

В личном кабинете участника реализованы следующие функции - ввод данных о себе и их редактирование, регистрация на гонки и удаление регистраций, возможность оставить комментарий к гонке и посмотреть все комментарии к гонке, просмотр всех актуальных гонок и переход на страницу с гонками и результатами.

## Модель участника гонок

В модель включены ФИО, команда, описание машины пользоветеля, инфо о пользователе, опыт гонок (в годах) и гоночный класс. 

```python
class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_profile')
    full_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    car_description = models.TextField()
    participant_description = models.TextField()
    experience = models.IntegerField()
    race_class = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.full_name} - {self.team}"
```
## Представление личного кабинета 

В личном кабинете есть три основных карточки: информация о юзере с возможностью ее редактировать, регистрации участника с возможностью удалить их из списка и список всех гонок, на которые можно зарегистрироваться. 

```python
@login_required
def participant_dashboard(request):
    participant = get_object_or_404(Participant, user=request.user)
    registrations = Registration.objects.filter(participant=participant)
    races = Race.objects.all().order_by('date', 'start_time')  # Все гонки

    context = {
        'registrations': registrations,
        'races': races,
        'participant': participant,
    }
    return render(request, 'participant_dashboard.html', context)
```

### Представление регистрации и удаления регистраций 

register_for_race: позволяет участнику зарегистрироваться на конкретную гонку. Если регистрация уже существует, она не создается повторно, и выводится соответствующее сообщение. В конце функция перенаправляет пользователя на страницу его личного кабинета.
unregister_from_race: позволяет участнику отменить свою регистрацию на гонку. Если регистрация успешно удалена, выводится сообщение об успешном удалении, а если нет — генерируется ошибка 404, если регистрация не найдена или пользователь не имеет прав на её удаление. После выполнения перенаправляет пользователя на страницу личного кабинета.

```python
@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participant = get_object_or_404(Participant, user=request.user)

    registration, created = Registration.objects.get_or_create(participant=participant, race=race)

    if created:
        print("Регистрация успешно создана")
    else:
        print("Регистрация уже существовала")

    return redirect('participant_dashboard')

@login_required
def unregister_from_race(request, registration_id):
    try:
        registration = Registration.objects.get(id=registration_id, participant__user=request.user)
        registration.delete()
        print("Регистрация успешно удалена")
    except Registration.DoesNotExist:
        raise Http404("Регистрация не найдена или у вас нет прав на её удаление")

    return redirect('participant_dashboard')
```
### Представление пользователской информации 
Требуется авторизация пользователя и, если запрос на редактирование пришел методом POST, проверяем и сохраняем данные из формы. В случае успешного сохранения пользователя перенаправляет на страницу личного кабинета, а в случае ошибок отображаются сообщения с информацией об этих ошибках. Если запрос не POST, отображается форма для редактирования профиля с текущими данными участника и списком доступных команд.

```python
@login_required
def profile_data(request):
    participant = get_object_or_404(Participant, user=request.user)
    teams = Team.objects.all()  

    if request.method == "POST":
        form = ParticipantProfileForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            print("Форма сохранена!") 
            return redirect('participant_dashboard')
        else:
            print("Ошибки формы:", form.errors)  
    else:
        form = ParticipantProfileForm(instance=participant)

    return render(request, 'edit_profile.html', {
        'form': form,
        'participant': participant,
        'teams': teams  
    })
```
### Представление для вывода всех гонок 

Выводим все гонки в личном кабинете с сортировкой по дате и времени.

```python
def all_races(request):
    races = Race.objects.all().order_by('date', 'start_time')
    print(races) 
    return render(request, 'all_races.html', {'races': races})
```

## HTML-страница личного кабинета 
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Личный кабинет</title>
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

        .race-item, .table-row {
            background-color: #333;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #444;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .race-item a, .table-row a {
            color: #e10600;
            text-decoration: none;
            font-weight: bold;
        }

        .race-item a:hover, .table-row a:hover {
            color: #ff1e00;
        }

        .form-section label {
            color: #e10600;
            display: block;
            text-align: left;
            margin-bottom: 5px;
        }

        .form-section input, .form-section select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 5px;
            border: 1px solid #444;
            background-color: #333;
            color: #fff;
        }

        .form-section button {
            background-color: #e10600;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .form-section button:hover {
            background-color: #ff1e00;
        }

        .button-group {
            display: flex;
            gap: 10px;
        }
    </style>
</head>
<body>

    <div class="dashboard-container">
        
        <!-- Профиль участника -->
        <div class="card">
            <h3>Ваш профиль</h3>
            <div class="card-content">
                <p><strong>Имя:</strong> {{ participant.full_name }}</p>
                <p><strong>Команда:</strong> {{ participant.team }}</p>
                <p><strong>Описание автомобиля:</strong> {{ participant.car_description }}</p>
                <p><strong>Описание участника:</strong> {{ participant.participant_description }}</p>
                <p><strong>Опыт:</strong> {{ participant.experience }}</p>
                <p><strong>Класс гонки:</strong> {{ participant.race_class }}</p>
                
                <!-- Кнопка для редактирования -->
                <form method="get" action="{% url 'profile_data' %}">
                    <button type="submit">Редактировать данные</button>
                </form>
            </div>
        </div>

        <!-- Список зарегистрированных гонок -->
        <div class="card">
            <h3>Ваши регистрации на гонки</h3>
            <div class="card-content">
                {% if registrations %}
                    <ul>
                        {% for registration in registrations %}
                            <li class="race-item">
                                <span>Дата гонки: {{ registration.race.date }}</span>
                                <div class="button-group">
                                    <a href="{% url 'unregister_from_race' registration.id %}">Отменить</a>
                                    <a href="{% url 'add_comment' registration.race.id %}">Добавить комментарий</a>
                                    <a href="{% url 'race_comments' registration.race.id %}">Смотреть комментарии</a>
                                </div>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p>Вы пока не зарегистрированы ни на одну гонку.</p>
                {% endif %}
            </div>
        </div>

        <!-- Список доступных гонок -->
        <div class="card">
            <h3>Все доступные гонки</h3>
            <div class="card-content">
                {% if races %}
                    <div>
                        {% for race in races %}
                            <div class="table-row">
                                <span>{{ race.date }} {{ race.start_time }}</span>
                                <form action="{% url 'register_for_race' race.id %}" method="post" style="display: inline;">
                                    {% csrf_token %}
                                    <button type="submit">Зарегистрироваться</button>
                                </form>
                                <a href="{% url 'add_comment' race.id %}">Добавить комментарий</a>
                                <a href="{% url 'race_comments' race.id %}">Смотреть комментарии к гонке</a>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <p>Нет доступных гонок.</p>
                {% endif %}
            </div>
        </div>

        <!-- Кнопка для просмотра всех гонок и результатов -->
        <div class="card">
            <h3>Гонки и результаты</h3>
            <div class="card-content">
                <form method="get" action="{% url 'all_races' %}">
                    <button type="submit">Посмотреть гонки и результаты</button>
                </form>
            </div>
        </div>

    </div>

</body>
</html>
```