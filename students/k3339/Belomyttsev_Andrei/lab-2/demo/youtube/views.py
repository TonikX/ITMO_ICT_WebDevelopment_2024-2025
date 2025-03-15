from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import AddChannelForm, AddReviewForm
from .models import Channel, Review

import requests

def index(request):
  return render(request, 'index.html')

def top(request):
  # print(request.GET) # parameters / none for filter
  data = {'channels': Channel.objects.filter(is_approved=True).order_by('-subs')}
  return render(request, 'top.html', data)

def channel(request, channel_id):
  channel = get_object_or_404(Channel, channel_id=channel_id)
  form = AddReviewForm()
  reviews = Review.objects.filter(channel__channel_id=channel_id)
  return render(request, 'channel.html', {'channel': channel, 'form': form, 'reviews': reviews})

def page_not_found(request, exception):
  return HttpResponseNotFound('<h1>Page not found</h1>')

YT_API_KEY = 'XXX'
@login_required
def add_channel(request):
  if request.method == 'POST':
    form = AddChannelForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      print(cd)
      try:
        if '/channel/' in cd['url']:
          ytid = cd['url'][-24:]
          info = requests.get(f'https://youtube.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={ytid}&key={YT_API_KEY}').json()
          stat = info['items'][0]['statistics']
          icon = info['items'][0]['snippet']['thumbnails']
          ytid = info['items'][0]['id']

          # create or update_or_create
          Channel.objects.create(
            channel_id=ytid, 
            url='https://www.youtube.com/channel/' + ytid,
            title=info['items'][0]['snippet']['title'],
            views=int(stat["viewCount"]),
            subs=int(stat["subscriberCount"]),
            videos=int(stat["videoCount"]),
            lang=cd['lang'],
            category=cd['category'],
            theme=cd['theme'],
            icon_default=icon['default']['url'],
            icon_medium=icon['medium']['url'],
            icon_high=icon['high']['url'],
            description=info['items'][0]['snippet']['description'],
            user=request.user,
            is_approved=request.user.is_superuser, # staff
            # tags=tags.split(',') if tags else []
          )
      except Exception as e:
        print('Adding Error:', e)
      return HttpResponseRedirect(reverse('add-channel'))
  else:
    form = AddChannelForm()
    user_channels = Channel.objects.filter(user=request.user)
  return render(request, 'add_channel.html', {'form': form, 'channels': user_channels})

@login_required
def add_review(request, channel_id):
  if request.method == 'POST':
    form = AddReviewForm(request.POST)
    if form.is_valid() and not Review.objects.filter(user=request.user, channel__channel_id=channel_id).exists():
      review = form.save(commit=False)
      review.user = request.user
      review.channel = Channel.objects.get(channel_id=channel_id)
      review.save()
  return redirect(f'/youtube/channel/{channel_id}')