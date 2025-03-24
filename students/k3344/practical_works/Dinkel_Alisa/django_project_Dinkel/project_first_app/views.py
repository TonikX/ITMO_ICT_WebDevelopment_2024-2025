from django.http import Http404  # метод обработки ситуации, когда нет необходимых записей в бд (обработчик ошибок)
from django.shortcuts import render  # метод "запускает" созданную хтмл страницу и передает в нее указанные параметры
from project_first_app.models import CarOwner  # таблицу из модели данных models


def owner(request, owner_id):
    try:  # метод try-except - обработчик исключений
        # Получаем владельца по ID
        owner = CarOwner.objects.get(pk=owner_id)
        # pk - автоматически создается в джанго для любой таблицы в модели (оно есть у любого объекта из бд)
        # owner_id будет передан функции при её вызове.
        # переменной owner присваивается объект, полученный в результате выполнения запроса
        # аналогичного "select * from CarOwner where pk=owner_id"
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
        # исключение, которое будет вызвано, если блок try вернет значение False (не будут найдены записи в таблице)

    cars = owner.ownership_set.all()  # получаем все автомобили владельца, используя обратную связь через Ownership
    licenses = owner.driverlicense_set.all()  # получаем все права владельца через Driverlicense

    return render(request, 'owner.html', {'owner': owner, 'cars': cars, 'licenses': licenses})
    # данная строка рендерит хтмл страницу owner.html и передает в него объекты, которые в хтмл называются ''
