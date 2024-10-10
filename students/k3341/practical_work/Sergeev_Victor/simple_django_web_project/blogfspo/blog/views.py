from django.shortcuts import render
from django.http import Http404, HttpResponse
from blog.models import CarOwner

def detail(request, owner_id):
    try:
        p = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        print('lol')
        raise Http404('no such car owner')

    return render(request, 'templates/owner.html', {'owner': p})
