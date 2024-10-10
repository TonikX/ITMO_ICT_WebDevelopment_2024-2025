from django.shortcuts import render


def index(request):
    return render(request, 'base.html', {'main_content': 'base page'})
