from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conference, AuthorRegistration, Review
from .forms import RegistrationForm, ReviewForm

def home(request):
    """Главная страница со списком конференций"""
    conferences = Conference.objects.all()
    return render(request, 'conference_app/home.html', {'conferences': conferences})

def conference_detail(request, conference_id):
    """Детальная страница конференции"""
    conference = get_object_or_404(Conference, id=conference_id)
    registrations = AuthorRegistration.objects.filter(conference=conference)
    reviews = Review.objects.filter(conference=conference)

    # Определяем регистрацию текущего пользователя (если он аутентифицирован)
    user_registration = None
    if request.user.is_authenticated:
        user_registration = registrations.filter(user=request.user).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.conference = conference
            registration.save()
            messages.success(request, "Вы успешно зарегистрировались на конференцию.")
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = RegistrationForm()

    return render(request, 'conference_app/conference_detail.html', {
        'conference': conference,
        'registrations': registrations,
        'reviews': reviews,
        'reg_form': form,
        'user_registration': user_registration,  # передаем в шаблон
    })

from .forms import ReviewForm  # убедитесь, что импорт формы выполнен

@login_required
def add_review(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    review_exists = Review.objects.filter(user=request.user, conference=conference).exists()

    if request.method == 'POST':
        if review_exists:
            messages.warning(request, "Вы уже оставляли отзыв для этой конференции.")
            return redirect('conference_detail', conference_id=conference.id)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен.")
            return redirect('conference_detail', conference_id=conference.id)
        else:
            messages.error(request, "Проверьте правильность заполнения формы.")
    else:
        form = ReviewForm()
        
    return render(request, 'conference_app/add_review.html', {
        'conference': conference,
        'review_exists': review_exists,
        'form': form,
    })


@login_required
def edit_registration(request, reg_id):
    registration = get_object_or_404(AuthorRegistration, id=reg_id, user=request.user)
    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация обновлена!")
            return redirect('conference_detail', conference_id=registration.conference.id)
    else:
        form = RegistrationForm(instance=registration)
    return render(request, 'conference_app/edit_registration.html', {'form': form, 'registration': registration})

@login_required
def delete_registration(request, reg_id):
    """Удаление регистрации пользователя"""
    registration = get_object_or_404(AuthorRegistration, id=reg_id, user=request.user)

    if request.method == "POST":
        conference_id = registration.conference.id
        registration.delete()
        messages.success(request, "Регистрация удалена!")
        return redirect('conference_detail', conference_id=conference_id)

    return render(request, 'conference_app/delete_registration.html', {'registration': registration})

def user_register(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'conference_app/register.html', {'form': form})

def participants_table(request):
    """Таблица участников конференций"""
    conferences = Conference.objects.prefetch_related('registrations').all()
    return render(request, 'conference_app/participants_table.html', {'conferences': conferences})

def custom_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа