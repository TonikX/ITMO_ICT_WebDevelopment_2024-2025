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
  # tags = ...

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