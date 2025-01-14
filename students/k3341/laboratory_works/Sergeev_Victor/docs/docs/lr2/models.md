# Модели

Для работы приложения используется база данных SQlite через Django ORM.

## Участник

Название: Participant

- first_name - имя участника, тип char, максимальная длина 50, not null
- last_name - фамилия участника, тип char, максимальная длина 50, not null
- email - электронная почта участника, тип char, максимальная длина 50, not null
- birth_date - день рождения участника, тип date
- profile_picture - фотография профиля участника, тип url
- country - страна участника, тип char, максимальная длина 50
- user - пользователь в фреймворке django, ассоциированный с участником, внешний ключ на user, обязательное поле

```python
class Participant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default='')
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

## Конференция

Название: Conference

- name - название конференции, тип char, максимальная длина 150, обязателен
- creator - создатель конференции, внешний ключ к Participant, обязателен
- description - описание конференции, тип char, максимальная длина 500
- participate_conditionals - условия участия в конференции, тип char, максимальная длина 500
- location - место проведения конференции, тип char, максимальная длина 150, обязателен
- date_of_start - время и дата начала конференции, тип datetime, обязателен
- date_of_finish - время и дата конца конференции, тип datetime, обязателен
- auditors - список слушателей конференции, тип manyToMany с моделью Participant через модель ConferenceAuditor
- speakers - список выступающих конференции, тип manyToMany с моделью Participant через модель ConferencePerformance

```python
class Conference(models.Model):
    name = models.CharField(max_length=150)
    creator = models.ForeignKey(Participant, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    participate_conditionals = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=150)
    date_of_start = models.DateTimeField()
    date_of_finish = models.DateTimeField()
    auditors = models.ManyToManyField(Participant, through='ConferenceAuditor', related_name='conference_auditors')
    speakers = models.ManyToManyField(Participant, through='ConferencePerformance', related_name='conference_speakers')
```

## Слушатель конференции

Название - ConferenceAuditor

- conference - конференция, ассоциированная с записью, внешний ключ к Conference, обязателен
- auditor - участник, ассоциированный с записью, внешний ключ к Participant, обязателен

Служит таблицей для отношения ManyToMany между Conference и Participant

```python
class ConferenceAuditor(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    auditor = models.ForeignKey(Participant, on_delete=models.CASCADE)
```

## Выступление

Название - ConferencePerformance

- conference - конференция, ассоциированная с записью, внешний ключ к Conference, обязателен
- speaker - участник, ассоциированный с записью, внешний ключ к Participant, обязателен
- speaking_topic - название выступления, тип char, максимальная длина 200, обязателен
- recommended - рекомендован к публикации или нет, тип boolean, обязателен, по умолчанию False

```python
class ConferencePerformance(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Participant, on_delete=models.CASCADE)
    speaking_topic = models.CharField(max_length=200)
    recommended = models.BooleanField(default=False)
```

## Отзыв к конференции

Название - Review

- grade - численная оценка от 1 до 10 конференции, тип positiveSmallInteger, число от 1 до 10 включительно, обязателен
- description - содержание отзыва, тип char, максимальная длина 1000
- conference - конференция, к которой написан отзыв, внешний ключ к Conference, обязателен
- author - автор отзыва, внешний ключ к Participant, обязателен
- date - дата и время последнего изменения отзыва, тип datetime, обязателен, по умолчанию timezone.now()

```python
class Review(models.Model):
    grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    description = models.CharField(max_length=1000, verbose_name='Speaking topic')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
```

## Комментарий к отзыву

Название - Commentary

- review - отзыв, к которому написан комментарий, внешний ключ к Review, обязателен
- author - автор комментария, внешний ключ к Participant, обязателен
- description - содержание комментария, тип char, максимальная длина 600, обязателен
- date - дата и время создания комментария, тип datetime, обязателен, по умолчанию timezone.now()

```python
class Commentary(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(Participant, on_delete=models.CASCADE)
    description = models.CharField(max_length=600)
    date = models.DateTimeField(default=timezone.now)
```
