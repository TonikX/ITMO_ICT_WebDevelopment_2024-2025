# Представления (Views)

## Классовые представления

### RaceListView
Отображает список всех активных гонок.

```python
class RaceListView(ListView):
    model = Race
    template_name = 'racing_app/race_list.html'
    context_object_name = 'races'
    queryset = Race.objects.filter(is_active=True)
```

### RaceDetailView
Показывает детальную информацию о гонке с комментариями.

```python
class RaceDetailView(DetailView):
    model = Race
    template_name = 'racing_app/race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['registration_form'] = RaceRegistrationForm()
        context['comment_form'] = CommentForm()
        return context
```

### RaceRegistrationView
Обрабатывает регистрацию пользователя на гонку.

```python
class RaceRegistrationView(LoginRequiredMixin, CreateView):
    model = RaceRegistration
    form_class = RaceRegistrationForm
    template_name = 'racing_app/race_registration.html'

    def form_valid(self, form):
        form.instance.racer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('race_detail', kwargs={'pk': self.object.race.pk})
```

## Функциональные представления

### user_profile
Отображает профиль пользователя с его регистрациями.

```python
@login_required
def user_profile(request):
    registrations = RaceRegistration.objects.filter(racer=request.user)
    return render(request, 'racing_app/user_profile.html', {
        'registrations': registrations
    })
```

### add_comment
Добавляет комментарий к гонке.

```python
@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.race = race
            comment.save()
            return redirect('race_detail', pk=race_id)
    return redirect('race_detail', pk=race_id)
```

## URL-маршруты

```python
# racing_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RaceListView.as_view(), name='race_list'),
    path('race/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('race/<int:race_id>/register/', views.RaceRegistrationView.as_view(), name='race_register'),
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/', views.user_profile, name='user_profile'),
]
```