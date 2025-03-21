# Документация к представлениям

Этот файл описывает представления, используемые в проекте.

## 1. Представление для регистрации

Функционал: регистрация пользователей в системе

```python
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
```

## 2. Представление для списка конференций

Функционал: отображение списка всех конференций

```python
def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, 'conference_list.html', {'conferences': conferences})
```

## 3. Представление для регистрации на презентацию

Функционал: регистрация пользователя на презентацию в рамках конкретной конференции

```python
def register_for_presentation(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.conference = conference
            registration.save()
            return redirect('conference_list')
    else:
        form = PresentationRegistrationForm()
    return render(request, 'register_presentation.html', {'form': form, 'conference': conference})
```

## 4. Представление для добавления отзыва

Функционал: добавление отзыва пользователя к конкретной конференции

```python
def add_review(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'conference': conference})
```

## 5. Представление для домашней страницы

Функционал: отображение домашней страницы приложения

```python
def home(request):
    return render(request, 'home.html')
```

## 6. Представление для кастомного входа в систему

Функционал: аутентификация пользователя и вход в систему

```python
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'login.html')
```

## 7. Представление для деталей конференции

Функционал: отображение подробной информации о конференции, включая отзывы и зарегистрированные презентации

```python
def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    reviews = Review.objects.filter(conference=conference)
    presentations = PresentationRegistration.objects.filter(conference=conference)
    return render(request, 'conference_detail.html', {
        'conference': conference,
        'reviews': reviews,
        'presentations': presentations,
    })
```

## 8. Представление для регистрации презентации (требует авторизации)

Функционал: регистрация презентации пользователем для конкретной конференции. Доступно только авторизованным пользователям.

```python
@login_required
def register_presentation(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.conference = conference
            presentation.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = PresentationRegistrationForm()
    return render(request, 'register_presentation.html', {'form': form, 'conference': conference})
```

## 9. Представление для профиля пользователя (требует авторизации)

Функционал: отображение профиля пользователя и списка зарегистрированных им презентаций. Доступно только авторизованным пользователям.

```python
@login_required
def profile(request):
    user = request.user
    presentations = PresentationRegistration.objects.filter(user=user)
    return render(request, 'profile.html', {
        'user': user,
        'presentations': presentations,
    })
```

## 10. Представление для редактирования презентации (требует авторизации)

Функционал: редактирование зарегистрированной презентации пользователем. Доступно только авторизованным пользователям и только для их собственных презентаций.

```python
@login_required
def edit_presentation(request, presentation_id):
    presentation = get_object_or_404(PresentationRegistration, id=presentation_id, user=request.user)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PresentationRegistrationForm(instance=presentation)
    return render(request, 'edit_presentation.html', {'form': form, 'presentation': presentation})
```

## 11. Представление для удаления презентации (требует авторизации)

Функционал: удаление зарегистрированной презентации пользователем. Доступно только авторизованным пользователям и только для их собственных презентаций.

```python
@login_required
def delete_presentation(request, presentation_id):
    presentation = get_object_or_404(PresentationRegistration, id=presentation_id, user=request.user)
    if request.method == 'POST':
        presentation.delete()
        return redirect('home')
```