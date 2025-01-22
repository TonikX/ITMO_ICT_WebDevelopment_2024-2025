from django.shortcuts import get_object_or_404, render

from .models import Car


def car_owner_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    ownership = car.ownership_set.first()  # Получаем первую запись о владении
    car_owner = ownership.car_owner if ownership else None

    return render(request, 'car_owner.html', {'car_owner': car_owner, 'car': car})
