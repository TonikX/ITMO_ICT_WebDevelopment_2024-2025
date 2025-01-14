# Лабораторная работа 2. Реализация простого сайта на django.

Вариант задания 5: Список научных конференций.

Интерфейс описывает названия конференций, список тематик, место проведения,
период проведения, описание конференций, описание место проведения, условия участия.
Необходимо реализовать следующий функционал:

* Регистрация новых пользователей.
* Просмотр конференций и регистрацию авторов для выступлений.
Пользователь должен иметь возможность редактирования и удаления своих
регистраций.
* Написание отзывов к конференциям. При добавлении комментариев,
должны сохраняться даты конференции, текст комментария, рейтинг (1-10),
информация о комментаторе.
* Администратор должен иметь возможность указания результатов
выступления (рекомендован к публикации или нет) средствами Django-
admin.
* В клиентской части должна формироваться таблица, отображающая всех
участников по конференциям.


1. Создаем модели:
```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class Conference(models.Model):
    title = models.CharField(max_length=300)
    themes = models.TextField(help_text="Список тем конференции")
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    location_description = models.TextField()

    def __str__(self):
        # Отображать название конференции и даты проведения
        return f"{self.title} ({self.start_date} - {self.end_date})"


class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Отображать пользователя, конференцию и оценку
        return f"Review by {self.user} for {self.conference} (Rating: {self.rating})"


class Participant(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)

    def __str__(self):
        # Отображать пользователя и конференцию
        return f"{self.user} - {self.conference}"


class Results(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Result"  # Название в единственном числе
        verbose_name_plural = "Results"  # Название во множественном числе

    def __str__(self):
        # Отображать участника и статус принятия
        status = "Accepted" if self.accepted else "Not Accepted"
        return f"{self.participant} - {status}"
```
Не забываем создать миграции:
```python
python manage.py makemigrations
python manage.py migrate
```

2. Создаем админ-панель:

```python
from django.contrib import admin
from .models import User, Conference, Review, Participant, Results

admin.site.register(User)
admin.site.register(Conference)
admin.site.register(Review)
admin.site.register(Participant)
admin.site.register(Results)
```

3. Добавляем в settings.py наше приложение:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'conferences_app',
]
```
А также
```python
AUTH_USER_MODEL = 'conferences_app.User'
```
4. Создаем суперпользователя:

```python
python manage.py createsuperuser
```

5. Создание контроллеров:
```python
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.contrib.auth import get_user_model
from .forms import AuthentificationCustomForm, NewUserForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Conference, Participant
from .forms import ReviewForm

User = get_user_model()


# для регистрации нового пользователя
class UserRegistrationView(CreateView):
    form_class = NewUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')


# для входа пользователя
class LoginView(View):
    form_class = AuthentificationCustomForm
    template_name = 'login.html'
    success_url = reverse_lazy('login')


# главная страница
class MainView(TemplateView):
    template_name = 'main.html'


class ConferenceListView(ListView):
    model = Conference
    template_name = 'conference_list.html'
    context_object_name = 'conferences'
    paginate_by = 4

    # поиск по конференциям
    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Conference.objects.all()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(themes__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query'] = query_params.urlencode()
        return context


class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conference_detail.html'
    context_object_name = 'conference'

    def dispatch(self, request, *args, **kwargs):
        # проверка на авторизацию
        if not request.user.is_authenticated:
            messages.info(request, "Зарегистрируйтесь для просмотра деталей конференции")
            return redirect(reverse('conference_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = self.get_object()
        context['reviews'] = conference.review_set.select_related('user').all()
        context['review_form'] = ReviewForm()
        context['is_author'] = self.request.user.is_staff
        return context

    def post(self, request, *args, **kwargs):
        conference = self.get_object()
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.date = conference.start_date
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен!")
            return redirect('conference_detail', pk=conference.pk)
        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)


class ParticipantRegistrationView(View):
    def post(self, request, pk):
        conference = get_object_or_404(Conference, pk=pk)
        if Participant.objects.filter(user=request.user, conference=conference).exists():
            messages.error(request, "Вы уже зарегистрированы на данную конференцию как участник.")
        else:
            Participant.objects.create(user=request.user, conference=conference, is_author=False)
            request.session['is_author'] = False
            messages.success(request, "Вы успешно зарегистрированы как участник!")
        return redirect('conference_list')


class AuthorRegistrationView(View):
    def post(self, request, pk):
        conference = get_object_or_404(Conference, pk=pk)
        if Participant.objects.filter(user=request.user, conference=conference).exists():
            messages.error(request, "Вы уже зарегистрированы на данную конференцию как автор.")
        else:
            Participant.objects.create(user=request.user, conference=conference, is_author=True)
            request.session['is_author'] = True
            messages.success(request, "Вы успешно зарегистрированы как автор!")
        return redirect('conference_list')


# все участники конференции
class AllParticipantsListView(ListView):
    model = Conference
    template_name = 'all_participants_list.html'
    context_object_name = 'conferences'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participants = Participant.objects.select_related('user', 'conference').all()
        participant_data = [
            {
                'conference': participant.conference.title,
                'date': participant.conference.start_date,
                'first_name': participant.user.first_name,
                'last_name': participant.user.last_name
            }
            for participant in participants
        ]
        context['participants'] = participant_data
        return context


# список конференций, на которые зарегистрирован текущий пользователь
class UserDashboardView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'user_cabinet.html'
    context_object_name = 'user_participants'

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user).select_related('conference')

    # удаление регистрации
    def post(self, request):
        participant_id = request.POST.get("participant_id")
        participant = Participant.objects.filter(id=participant_id, user=request.user).first()
        if participant:
            participant.delete()
            messages.success(request, "Регистрация успешно удалена.")
        else:
            messages.error(request, "Регистрация не найдена или у вас нет прав для её удаления.")
        return redirect('user_dashboard')
```

5. Работа с адресацией:
```python
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegistrationView, AllParticipantsListView, ConferenceListView, ConferenceDetailView, \
    MainView, UserDashboardView, AuthorRegistrationView, ParticipantRegistrationView

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
    path('conferences/<int:pk>/', ConferenceDetailView.as_view(), name='conference_detail'),
    path('conference/<int:pk>/participant/register/', ParticipantRegistrationView.as_view(), name='participant_registration'),
    path('conference/<int:pk>/author/register/', AuthorRegistrationView.as_view(), name='author_registration'),
    path('participants/', AllParticipantsListView.as_view(), name='all_participants_list'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
]
```

6. Создаем формы:
```python
from django import forms
from .models import Review, Participant, User, Results
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Для добавления отзывов
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        labels = {
            'comment': 'Комментарий',
            'rating': 'Оценка',
        }


# для добавления участников
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all(), required=True)


# для регистрации нового пользователя
class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'email']
        labels = {
            'username': 'Никнейм',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
            'email': 'Email'
        }


# для аутентификации
class AuthentificationCustomForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']


# для добавления результатов
class ResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = ['accepted']
```
6. Доделываем работу на макс. балл:
* С помощью bootstrap реализовано меню
* Реализована пагинация страниц списка конференций
* Сделан поиск по конференциям