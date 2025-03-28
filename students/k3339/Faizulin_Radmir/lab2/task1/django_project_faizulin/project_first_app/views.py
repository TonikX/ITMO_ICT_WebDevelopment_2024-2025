from django.shortcuts import render
from .models import Owner

def owner_detail(request, id_owner):
    owner = Owner.objects.get(pk=id_owner)
    context = {
        'name': owner.name,
        'surname': owner.surname,
        'birth_day': owner.birth_day,
    }
    return render(request, 'owner.html', context)
