from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login, logout


from .forms import CustomUserCreationForm, AddRace, AddCommentForm, AddDriver, AddCar, AddTruck
from .models import User, Driver, Race, Truck, Comments


def is_admin(user):
    return user.is_superuser


def show_user(request, user_slug):
    user = get_object_or_404(User, slug=user_slug)
    return render(request, 'score/show_user.html', {'user': user})



def show_driver(request, driver_slug):
    driver = get_object_or_404(Driver, slug=driver_slug)
    car = driver.car_id
    return render(request, 'score/driver_details.html', {'driver': driver, 'car': car})



def show_drivers(request):
    query = request.GET.get('q', '')
    drivers_list = Driver.objects.all().order_by('id')
    if query:
        drivers_list = drivers_list.filter(first_name__icontains=query) | drivers_list.filter(
            last_name__icontains=query)
    paginator = Paginator(drivers_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'score/drivers.html', {'page_obj': page_obj, 'query': query})



def detail_race(request, race_id):
    sort = request.GET.get('sort', 'end_position')
    order = request.GET.get('order', 'asc')
    sort_order = sort if order == 'asc' else f'-{sort}'
    races = Race.objects.filter(truck_id=race_id).select_related('Driver_id', 'truck_id').order_by(sort_order)
    paginator = Paginator(races, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            race_instance = get_object_or_404(Race, pk=race_id)# Тту мы получаем сам объект а не его номер  так как если бы был номер то
            # так как если бы был номер то выходит ошибка внешний ключ работает с объектом а не id
            comment.race_id = race_instance
            comment.user_id = request.user
            comment.date = timezone.now()
            comment.save()
            return redirect('detail_race', race_id=race_id)
    else:
        form = AddCommentForm()
    comments = Comments.objects.filter(race_id=race_id)
    return render(request, 'score/race_details.html',
                  {'page_obj': page_obj, 'form': form, 'comments': comments, 'sort': sort, 'order': order})



@user_passes_test(is_admin)
def add_driver(request):
    if request.method == 'POST':
        form = AddDriver(request.POST)
        if form.is_valid():
            driver = form.save()
            return redirect('show_driver', driver_slug=driver.slug)
    else:
        form = AddDriver()
    return render(request, 'score/new_object.html', {'form': form})



@user_passes_test(is_admin)
def add_car(request):
    if request.method == 'POST':
        form = AddCar(request.POST)
        if form.is_valid():
            form.save()
            return redirect('drivers')
    else:
        form = AddCar()
    return render(request, 'score/new_object.html', {'form': form})


@user_passes_test(is_admin)
def add_race(request):
    if request.method == 'POST':
        form = AddRace(request.POST)
        if form.is_valid():
            form.save()
            return redirect('races')
    else:
        form = AddRace()
    return render(request, 'score/new_object.html', {'form': form})


@user_passes_test(is_admin)
def add_truck(request):
    if request.method == 'POST':
        form = AddTruck(request.POST)
        if form.is_valid():
            form.save()
            return redirect('races')
    else:
        form = AddTruck()
    return render(request, 'score/new_object.html', {'form': form})


def show_races(request):
    races = Truck.objects.all()
    return render(request, 'score/show_races.html', {'races': races})


def show_users(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'score/users.html', {'page_obj': page_obj})


@login_required
def profile_view(request):
    return render(request, 'score/profile.html', {'user': request.user})


# View for user signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('races')
    else:
        form = CustomUserCreationForm()
    return render(request, 'score/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'score/login.html'
