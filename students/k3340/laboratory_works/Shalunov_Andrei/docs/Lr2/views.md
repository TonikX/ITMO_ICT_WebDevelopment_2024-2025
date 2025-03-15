# Лабораторная работа №2 – Табло победителей автогонок

## Описание представлений

В данном проекте реализованы представления, обеспечивающие взаимодействие с пользователями, регистрацию на гонки, добавление комментариев и управление профилем. Ниже приведены основные классовые представления, используемые в приложении.

---

### 1. `UserRegistrationView`
Представление для регистрации нового пользователя.

```python
from django.contrib.auth import login
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django.urls import reverse_lazy

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('race_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
```
Описание: Используется для создания нового пользователя. При успешной регистрации пользователь сразу авторизуется в системе.

Шаблон: registration/register.html
###2. LogoutUser
Представление для выхода пользователя из системы.

```python
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('race_list')
```
Описание: Завершает сеанс пользователя и перенаправляет его на список гонок.

Маршрут: race_list
###3. RaceListView
Представление для отображения списка предстоящих и прошедших гонок.

```python
from django.utils import timezone
from django.views.generic import ListView
from .models import Race

class RaceListView(ListView):
    model = Race
    template_name = 'race_list.html'
    context_object_name = 'races'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['upcoming_races'] = Race.objects.filter(date__gte=now).order_by('-date')
        context['past_races'] = Race.objects.filter(date__lt=now).exclude(result="").order_by('-date')
        return context
```
Описание: Отображает две категории гонок — предстоящие и прошедшие.

Шаблон: race_list.html
###4. RaceDetailView
Представление для отображения деталей конкретной гонки.

```python
from django.views.generic import DetailView
from .models import Race, RaceResult, Registration
from .forms import UnregisterForm

class RaceDetailView(DetailView):
    model = Race
    template_name = 'race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['is_upcoming'] = self.object.date >= now
        if context['is_upcoming']:
            context['registered_racers'] = self.object.registrations.all()
        else:
            context['race_results'] = RaceResult.objects.filter(race=self.object).order_by('place')
        context['unregister_form'] = UnregisterForm()
        return context
```
Описание: Показывает информацию о гонке, включая зарегистрированных участников и результаты.

Шаблон: race_detail.html
###5. RaceRegistrationView
Представление для регистрации гонщика на гонку.

```python
from django.views.generic import CreateView
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404, reverse
from .models import Race, Registration

class RaceRegistrationView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'register_race.html'

    def form_valid(self, form):
        race = get_object_or_404(Race, id=self.kwargs['race_id'])
        form.instance.race = race
        form.instance.racer = self.request.user.racer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('race_detail', args=[self.kwargs['race_id']])
```
Описание: Позволяет гонщику зарегистрироваться на конкретную гонку.

Шаблон: register_race.html
###6. RaceUnregisterView
Представление для отмены регистрации гонщика на гонку.

```python
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Race, Registration

class RaceUnregisterView(View):
    def post(self, request, *args, **kwargs):
        race = get_object_or_404(Race, id=self.kwargs['race_id'])
        registration = Registration.objects.filter(race=race, racer=request.user.racer).first()
        if registration:
            registration.delete()
        return redirect('race_detail', pk=race.id)
```
Описание: Позволяет пользователю отменить свою регистрацию на гонку.

Маршрут: race_detail
###7. RacerProfileCreateView
Представление для создания профиля гонщика.

```python
from django.views.generic import CreateView
from .forms import RacerProfileForm

class RacerProfileCreateView(CreateView):
    model = Racer
    template_name = 'create_racer_profile.html'
    form_class = RacerProfileForm
    success_url = reverse_lazy('race_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
```
Описание: Позволяет пользователю создать профиль гонщика.

Шаблон: create_racer_profile.html
###8. RacerProfileView
Представление для отображения профиля гонщика.

```python
from django.views.generic import DetailView
from .models import Racer

class RacerProfileView(DetailView):
    model = Racer
    template_name = 'racer_profile.html'
    context_object_name = 'racer'

    def get_object(self):
        return get_object_or_404(Racer, user=self.request.user)
```
Описание: Показывает информацию о профиле гонщика, включая список его автомобилей.

Шаблон: racer_profile.html
###9. CommentCreateView
Представление для добавления комментария к гонке.

```python
from django.views.generic import CreateView
from .forms import CommentForm
from django.shortcuts import get_object_or_404, reverse
from .models import Race, Comment

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.race = get_object_or_404(Race, id=self.kwargs['race_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('race_detail', args=[self.kwargs['race_id']])
```
Описание: Позволяет пользователю оставить комментарий к гонке.

Шаблон: add_comment.html
###10. EditRaceView
Представление для редактирования информации о гонке (только для администраторов).

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from .models import Race

class EditRaceView(UserPassesTestMixin, UpdateView):
    model = Race
    fields = ['name', 'date', 'result']
    template_name = 'edit_race.html'
    success_url = reverse_lazy('race_list')

    def test_func(self):
        return self.request.user.is_staff
```
Описание: Позволяет администратору редактировать информацию о гонке.

Шаблон: edit_race.html
###11. DeleteRaceView
Представление для удаления гонки (только для администраторов).

```python
class DeleteRaceView(UserPassesTestMixin, DeleteView):
    model = Race
    template_name = 'delete_race.html'
    success_url = reverse_lazy('race_list')

    def test_func(self):
        return self.request.user.is_staff
```
Описание: Позволяет администратору удалить гонку.

Шаблон: delete_race.html
###12. DeleteCommentView
Представление для удаления комментария (только для администраторов).

```python
class DeleteCommentView(UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        race_id = comment.race.id
        if request.user.is_staff:
            comment.delete()
        return redirect('race_detail', pk=race_id)

    def test_func(self):
        return self.request.user.is_staff
``` 
Описание: Позволяет администратору удалить комментарий к гонке.

Маршрут: race_detail