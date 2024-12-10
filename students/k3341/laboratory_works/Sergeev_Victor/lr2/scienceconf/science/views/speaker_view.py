from django.http import HttpResponseForbidden
from django.views.generic import edit
from django.views import View
from django.db import transaction
from django.shortcuts import render, redirect
from science import models, forms

class SpeakerCreate(View):
    http_method_names = ['get', 'post']

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        context = {'form': forms.SpeakerRegisterForm}
        conf_id = kwargs['pk']
        conference = models.Conference.objects.filter(id=conf_id)
        context['conf'] = conference

        return render(request, 'static/templates/speaker/speaker_create.html', context)

    @transaction.atomic
    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        context = {}
        form = forms.SpeakerRegisterForm(request.POST or None)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'static/templates/speaker/speaker_create.html', context)

        conference_id = kwargs['pk']
        user_id = request.user.id
        conference = models.Conference.objects.filter(id=conference_id)[0]
        speaker = models.Participant.objects.filter(user__id=user_id)[0]

        models.ConferencePerformance.objects.create(
            conference = conference,
            speaker = speaker,
            speaking_topic = form.cleaned_data['topic']
        )
        return redirect(f'/conference/{conference_id}/')

class SpeakerUpdate(edit.UpdateView):
    model = models.ConferencePerformance
    fields = ['speaking_topic', 'recommended']
    template_name = 'static/templates/speaker/speaker_update.html'
    def get_object(self, **kwargs):
        performance_pk = self.kwargs.get('pk')
        object = models.ConferencePerformance.objects.filter(id=performance_pk).first()
        return object
        
    def get_success_url(self):
        object = self.get_object()
        return f'/conference/{object.conference.id}'
    
    def get(self, request, *args: str, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args: str, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        
        return super().post(request, *args, **kwargs)

class SpeakerDelete(edit.DeleteView):
    model = models.ConferencePerformance
    template_name = 'static/templates/speaker/speaker_delete.html'
    def get_object(self, **kwargs):
        conference_id = self.kwargs.get('pk')
        object = models.ConferencePerformance.objects.filter(conference__id=conference_id).first()
        return object

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        object = self.get_object()
        context = {'object': object}
        return render(request, 'static/templates/speaker/speaker_delete.html', context)

    def get_success_url(self):
        object = self.get_object()
        return f'/conference/{object.conference.id}'
    
    def post(self, request, *args: str, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
        return super().post(request, *args, **kwargs)