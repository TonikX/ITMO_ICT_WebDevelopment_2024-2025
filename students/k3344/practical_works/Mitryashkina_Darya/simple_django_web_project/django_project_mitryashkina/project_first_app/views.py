from django.shortcuts import render
from django.http import Http404 

from .models import Owner

# Create your views here.
def owner_info(request, id):
    try:
        owner = Owner.objects.get(pk=id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    
    context = {'owner': owner}
    return render(request, 'owner.html', context)
