# Лабораторная работа 2

## Задание

### Лабораторная часть

Реализовать веб сервис, в соответствии с вариантом из задания (студент с порядковым номером 6 в списке группы делает 6 вариант, седьмой - вариант номер 1).<br>
Текст лабораторной работы [тут](https://drive.google.com/file/d/1kp4xcF-6r-g5jvephy69n9XvS-7hU4KT/view?usp=sharing).<br>
Срок сдачи: **** (включительно)<br>

Обращаем внимание, что **доступна возможность предложить свой индивидуальный вариант** и делать работу по нему. <br>
Если Вы хотите индивидуальный враиант, советуем не использовать вариант из дисциплины "Адаптивный веб-дизайн" в этой работе, эффективнее Вы сможете его использовать в следующих работах.<br>

### Для получения максимального балла. 
Чтобы продлить срок, необходимо:
- Реализовать меню (меню с бутсрап - https://www.youtube.com/watch?v=HEPTgggsRgY)
- Реализвать пагинацию страниц (так себе вариант - https://evileg.com/ru/post/10/ , отличный вариант - https://evileg.com/ru/post/237/)
- Внедрить поиск по объектам, с которыми настроена пагинация (https://evileg.com/ru/post/21/)

### Полезные материалы

[Фундаментально](https://www.youtube.com/playlist?list=PLlWXhlUMyooaDkd39pknA1-Olj54HtpjX) - плейлист уроков по джанго для тех кто хочет **фундаментально** изучить, как работает джанго веб фремйворк и заниматься этим в будущем.

[Базово](https://www.youtube.com/playlist?list=PLF-NY6ldwAWqP4S95brtPHZ5fTCxilgei) - плейлист, который позволит **быстро** понять, как и что работает и **сделать лабу**.

### Сдача работы №2

Все файлы загрузить в папку **students/группа/laboratory_works/фамилия_имя/laboratory_work_2**. Инструкция о загрузке работы ниже. Не забывайте о файле gitignor.

Необходимо сделать отчет. Все отчеты делаются средствами markdown и mkdocs. Инструкция по созданию веб-страничек из markdown средствами mkdocs доступна тут в пункте 3.2.2 https://docs.google.com/document/d/1rIfREFvCB4pp8uF990Tz3PLXRJ5u_w-Y3vLxfXWKoxg/edit?usp=sharing . Краткое описание работы с markdown доступно в пункте 3.1

Как делать пул-реквест описано в разделе **[Сдача работ](https://github.com/TonikX/ITMO_ICT_WebDevelopment_2024-2025/blob/master/README.md#%D1%81%D0%B4%D0%B0%D1%87%D0%B0-%D1%80%D0%B0%D0%B1%D0%BE%D1%82)**

## Вариант

Cайт со списком образовательных и научно-популярных Ютуб каналов.

Хранится информация о каналах (id, url, title, views, subs, videos, lang, category, theme, icon, ...), пользователях, отзывах.

Необходимо реализовать следующий функционал:

- Регистрация пользователей
- Пользователь может добавлять новые каналы
- Написание отзывов к каналам с текстом и рейтингом
- Администратор должен иметь возможность одобрять добавление новых каналов средствами Django-admin
- Страница с топом каналов
- Страница канала с описанием и другой информацией
- Работа с API Ютуба

## Code

settings.py:
```python
...
INSTALLED_APPS = [
  ...
  'youtube',
  'users',
]
...
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Moscow'
...
LOGIN_URL = 'users:login'
```

urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('youtube/', include('youtube.urls')),
    path('users/', include('users.urls', namespace='users'))
]
handler404 = page_not_found
```

### YouTube App

admin.py:
```python
from django.contrib import admin

from .models import Channel, Review

class ChannelAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'is_approved', 'time_create')
  ordering = ('-time_create', 'title')
  list_editable = ('is_approved',)

class ReviewAdmin(admin.ModelAdmin):
  list_display = ('channel', 'user', 'rating', 'time_create')
  list_display_links = ('channel', 'user')
  ordering = ('-time_create', 'channel')

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Review, ReviewAdmin)
```

forms.py:
```python
from django import forms
from .models import Channel, Review

class AddChannelForm(forms.ModelForm):
  class Meta:
    model = Channel
    fields = ['url', 'lang', 'category', 'theme']

class AddReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ['rating', 'text']
```

urls.py:
```python
from django.urls import path, re_path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('top/', views.top, name='top'),
  re_path(r'^channel/(?P<channel_id>[a-zA-Z0-9_-]{24})/$', views.channel, name='channel'),
  path('channel/add/', views.add_channel, name='add-channel'),
  re_path(r'^add-review/(?P<channel_id>[a-zA-Z0-9_-]{24})/$', views.add_review, name='add-review'),
]
```

templatetags/youtube_tags.py
```python
from django import template

register = template.Library()

@register.filter()
def intformat(n):
  return ((f'{str(n)[:-9]}.{str(n)[-9]}B' if n >= 1000000000 else f'{str(n)[:-6]}.{str(n)[-6]}M') if n >= 1000000 else f'{str(n)[:-3]}.{str(n)[-3]}K') if n >= 1000 else n
```

models.py:
```python
from django.db import models
from django.urls import reverse
from django.conf import settings

class Channel(models.Model):
  CATEGORIES = (
    ('popsci', 'Научпоп'),
    ('edu', 'Образование'),
  )
  THEMES = (
    ('all', 'Разное'),
    ('it', 'IT'),
    ('programming', 'Программирование'),
    ('physics', 'Физика'),
    ('chemistry', 'Химия'),
    ('space', 'Космос'),
    ('math', 'Математика'),
    ('history', 'История'),
    ('biology', 'Биология'),
    ('medicine', 'Медицина'),
    ('geography', 'География'),
    ('electronics', 'Электроника'),
    ('social', 'Обществознание'),
    ('economics', 'Экономика'),
    ('english', 'Английский')
  )
  LANGS = (
    ('ru', '🇷🇺'),
    ('en', '🇺🇸'),
    # 'es': '🇪🇸',
    # 'de': '🇩🇪',
    # 'fr': '🇫🇷',
    # 'pt': '🇧🇷'
  )

  channel_id = models.CharField(max_length=24, unique=True, db_index=True, primary_key=True)
  url = models.CharField(max_length=100, unique=True) # 56
  title = models.CharField(max_length=255)
  views = models.PositiveBigIntegerField()
  subs = models.PositiveIntegerField()
  videos = models.PositiveIntegerField()
  lang = models.CharField(max_length=2, choices=LANGS) # default='ru'
  category = models.CharField(max_length=20, choices=CATEGORIES) # default='popsci'
  theme = models.CharField(max_length=20, choices=THEMES, default='all')
  icon_default = models.CharField(max_length=200) # 103
  icon_medium = models.CharField(max_length=200)
  icon_high = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  is_approved = models.BooleanField(default=False) # or null, 3 types?
  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, blank=True, null=True) # SET_NULL
  time_create = models.DateTimeField(auto_now_add=True)
  time_update = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('channel', kwargs={'channel_id': self.channel_id})

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
  channel = models.ForeignKey(Channel, models.CASCADE)
  rating = models.PositiveSmallIntegerField(choices=((i,i) for i in range(1, 11)))
  text = models.TextField(blank=True)
  time_create = models.DateTimeField(auto_now_add=True)
  time_update = models.DateTimeField(auto_now=True)
```

templates:
- base.html
- add_channel.html
- channel.html
- index.html
- top.html

base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title }}</title>
  <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1/new.min.css"> -->
  <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css"> -->
  <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css"> -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/light.min.css">
  <style>
    .avatar {
      border-radius: 50%;
      width: 100px;
      height: 100px;
    }
  </style>
</head>
<body>
  <header>
    <h1><a href="{% url 'home' %}">Educational YouTube</a></h1>
    <a href="{% url 'home' %}">Home</a> / 
    <a href="{% url 'top' %}">Top</a> / 
    <a href="{% url 'add-channel' %}">Add Channel</a> / 
    {% if user.is_authenticated %}
    <a href="{% url 'users:logout' %}">Log out</a> / {{ user.username }} 
    {% else %}
    <a href="{% url 'users:login' %}">Log in</a> / <a href="{% url 'users:register' %}">Register</a>
    {% endif %}
  </header>
{% block content %} {% endblock %}
</body>
</html>
```

add_channel.html
```html
{% extends 'base.html' %}
{% load youtube_tags %}

{% block content %}

<h2>Add Channel</h2>
<form action="" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>

<h3>My Channels ({{ channels|length }})</h3>
{% if channels %}
<table>
<tr>
  <th></th>
  <th>Channel</th>
  <th>Subs</th>
  <th>Status</th>
</tr>
{% for channel in channels %}
<tr>
  <td>
    <a href="{{ channel.get_absolute_url }}">
    <img src="{{ channel.icon_medium }}" width="40" height="40" style="margin-bottom: 0 !important; border-radius: 50% !important;"></a>
  </td>
  <td><a href="{{ channel.get_absolute_url }}">{{ channel.title }}</a></td>
  <td>{{ channel.subs|intformat }}</td>
  {% if channel.is_approved %}
  <td style="color:green;">Approved</td>
  {% else %}
  <td style="color:red;">Not Approved</td>
  {% endif %}
</tr>
{% endfor %}
</table>
{% endif %}

{% endblock %}
```

channel.html
```html
{% extends 'base.html' %}
{% load youtube_tags %}

{% block content %}
<h2>{{ channel.title }}</h2>
<a href="{{ channel.url }}" target="_blank"><img src="{{ channel.icon_high }}" class="avatar"></a>
<p>{{ channel.get_lang_display }} / {{ channel.get_category_display }} / {{ channel.get_theme_display }} /
{{ channel.subs|intformat }} subs / {{ channel.views|intformat }} views / {{ channel.videos|intformat }} videos
</p>
<p>{{ channel.description|linebreaks|urlize }}</p>
<p>Added by {{ channel.user.username|default:"anon" }} at {{ channel.time_create }}</p>

{% if user.is_authenticated %}
<h3>Write Review</h3>
<form action="/youtube/add-review/{{channel.channel_id}}/" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
<input type="submit">
</form>
{% endif %}

<h3>Reviews ({{ reviews|length }})</h3>
{% for review in reviews %}
<p><b>{{ review.rating }}</b> / <b>{{ review.user.username }}</b> / {{ review.time_create }}
{{ review.text|linebreaks }}</p>
{% if not forloop.last %}
<hr>
{% endif %}
{% endfor %}

{% endblock %}
```

index.html
```html
{% extends 'base.html' %}

{% block content %} 
<h2>Home</h2>
<p>На этом сайте собраны образовательные и научно-популярные <a href="{% url 'top' %}">ютуб каналы</a> на русском и английском языках.</p>
<p>После <a href="{% url 'users:register' %}">регистрации</a> или <a href="{% url 'users:login' %}">входа в аккаунт</a> вы сможете <a href="{% url 'add-channel' %}">предложить</a> свои каналы.</p>
<p>Вы также сможете оставлять отзывы на странице канала.</p>
{% endblock %}
```

top.html
```html
{% extends 'base.html' %}
{% load youtube_tags %}

{% block content %}
<h2>List of educational YouTube channels</h2>
<table>
<tr>
  <th></th>
  <th>Channel</th>
  <th>Subs</th>
  <th>Views</th>
  <th>Videos</th>
</tr>
{% for channel in channels %}
<tr>
  <td>
    <a href="{{ channel.get_absolute_url }}">
    <img src="{{ channel.icon_medium }}" width="40" height="40" style="margin-bottom: 0 !important; border-radius: 50% !important;"></a>
  </td>
  <td><a href="{{ channel.get_absolute_url }}">{{ channel.title }}</a></td>
  <td>{{ channel.subs|intformat }}</td>
  <td>{{ channel.views|intformat }}</td>
  <td>{{ channel.videos|intformat }}</td>
</tr>
{% endfor %}
</table>
{% endblock %}
```

### Users App

forms.py
```python
from django import forms
from django.contrib.auth import get_user_model

class LoginUserForm(forms.Form):
  username = forms.CharField(label='Login', widget=forms.TextInput())
  password = forms.CharField(label='Password', widget=forms.PasswordInput())

class RegisterUserForm(forms.ModelForm):
  username = forms.CharField(label='Login', widget=forms.TextInput())
  password = forms.CharField(label='Password', widget=forms.PasswordInput())
  password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput())

  class Meta:
    model = get_user_model()
    fields = ['username', 'password']

  def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
      raise forms.ValidationError("Passwords don't match")
    return cd['password']
```

urls.py
```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
  path('login/', views.login_user, name='login'),
  path('logout/', views.logout_user, name='logout'),
  path('register/', views.register, name='register'),
]
```

views.py
```python
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginUserForm, RegisterUserForm

def login_user(request):
  if request.method == 'POST':
    form = LoginUserForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request, username=cd['username'], password=cd['password'])
      if user and user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
  else:
    form = LoginUserForm()
  return render(request, 'users/login.html', {'form': form})

def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse('users:login'))

def register(request):
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return HttpResponseRedirect(reverse('users:login'))
  else:
    form = RegisterUserForm()
  return render(request, 'users/register.html', {'form': form})
```

login.html
```html
{% extends 'base.html' %}

{% block content %}

<h2>Log in</h2>
<form action="" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>

{% endblock %}
```

register.html
```html
{% extends 'base.html' %}

{% block content %}

<h2>Register</h2>
<form action="" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>

{% endblock %}
```