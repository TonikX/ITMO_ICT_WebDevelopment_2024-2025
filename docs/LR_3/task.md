## Реализация проекта по варианта в рамках лабораторной работы

После утверждения схемы данных, первым делом (после полноценной настройки проекта),
были созданы 8 основных моделей: Sport, Coach, Sportsman, Equipment, SportHall, EquipmentOfSportHall, SportSection, Schedule.
Примеры представлены ниже:
```
class Sport(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    type = models.CharField(max_length=1, choices=(('t', 'team'), ('i', 'individual')), verbose_name='Тип')
    equipment_needed = models.BooleanField(verbose_name='Надобность оборудования')


class Coach(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя тренера')
    last_name = models.TextField(max_length=50, verbose_name='Фамилия тренера')
    middle_name = models.TextField(max_length=50, verbose_name='Отчество тренера')
    gender = models.CharField(max_length=1, choices=(('m', 'male'), ('f', 'female')), verbose_name='Пол тренера')
    date_of_birth = models.DateField(verbose_name='Дата рождения тренера')
    qualification = models.TextField(max_length=100, verbose_name='Квалификация')
    experience = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Опыт работы')
```

Далее применила миграции и приступила к созданию views и serializers. В рамках данного этапа
была проведена полноценная подготовка к заполнению ранее созданных моделей:
```
class SportsmenAPIView(APIView):
    def get(self, request):
        sportsmen = Sportsman.objects.all()
        serializer = SportsmanSerializer(sportsmen, many=True)
        return Response({"Sportsmen": serializer.data})


class SportsmanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sportsman
        fields = "__all__"
```
Аналогичные классы были сделаны для всех моделей, после чего я приступила к заполнению. 
На скриншотах ниже придставлю примеры заполнения и готовые модели:
![Alt текст](images/1.png)
![Alt текст](images/2.png)
![Alt текст](images/3.png)
![Alt текст](images/4.png)
![Alt текст](images/5.png)
![Alt текст](images/6.png)
![Alt текст](images/7.png)

Теперь доработаем функционал, добавив удаление и редактирование определенных моделей:
Рассмотрим на примере спортсмена:
```
class SportsmenUpdateView(UpdateAPIView):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmenSerializer

    def get(self, request, *args, **kwargs):
        sportsmen = self.get_object()
        serializer = self.get_serializer(sportsmen)
        return Response(serializer.data)
        
        
class SportsmenDeleteView(DestroyAPIView):
    queryset = Sportsman.objects.all()
    serializer_class = SportsmenSerializer
```
Аналогичным образом были созданы view для остальных необходимых моделей. Результат приведем наскришоте ниже:
![Alt текст](images/8.png)
![Alt текст](images/9.png)

После базовой и обычной нстройки проекта приступим к реализации дополнительного функционала, который был прописан в описании варианта:
- Какая секция будет в заданном зале, в заданный день недели на заданное время?
![Alt текст](images/10.png)
- Сколько спортсменов занимаются в секции и какое количество свободных мест?
![Alt текст](images/11.png)
- Какое расписание тренировок у конкретного тренера?
![Alt текст](images/12.png)
- Какое оборудование имеется в наличии в определенном зале?
![Alt текст](images/13.png)
- Список доступных секций по конкретному виду спорта
![Alt текст](images/14.png)

 В финальной части лабораторной работы подключим регистрацию / авторизацию по токенам / вывод информации о текущем пользователе средствами Djoser.
 На скриншотах ниже будут представлены все запросы, которые выполнялись на осонове видео-урока)
 ![Alt текст](images/15.png)
 ![Alt текст](images/16.png)
 ![Alt текст](images/17.png)