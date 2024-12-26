from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Car
from .models import Owner
from .models import User
from .forms import CustomUserCreationForm

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

def owner_detail(request, owner_id):
    owner = get_object_or_404(Owner, pk=owner_id)
    return render(request, 'owner.html', {'owner': owner})

def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

def home(request):
    return render(request, 'home.html')  # Create a `home.html` template in the templates folder

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Переход к списку пользователей после создания
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


