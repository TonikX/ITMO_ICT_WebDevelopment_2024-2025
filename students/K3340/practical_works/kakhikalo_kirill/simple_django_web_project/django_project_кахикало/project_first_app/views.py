from django.http import Http404
from django.shortcuts import render
from project_first_app.models import AutoOwner
def detail(request, owner_id):
    try:
        p = AutoOwner.objects.get(pk=owner_id)
    except AutoOwner.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'owner.html', {'owner': p})
