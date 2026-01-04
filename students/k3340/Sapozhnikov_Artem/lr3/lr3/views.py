from django.shortcuts import render

def swagger_view(request):
    return render(request, "swagger.html")
