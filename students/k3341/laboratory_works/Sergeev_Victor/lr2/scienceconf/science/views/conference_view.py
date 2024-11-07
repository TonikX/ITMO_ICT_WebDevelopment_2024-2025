from django.views.generic import list, detail, edit
from django.views import View
from django.db import transaction
from django.shortcuts import render, redirect
from science import models, forms

class ConferenceList(list.ListView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_list.html'
    def get(self, request, **kwargs):
        conferences = models.Conference.objects.all()
        context = {'conf_list': conferences}
        return render(request, 'static/templates/conference/conference_list.html', context)

class ConferenceDetail(detail.DetailView):
    model = models.Conference
    def get(self, request, **kwargs):
        object = self.get_object()
        conference_id = kwargs['pk']
        speakers = models.ConferencePerformance.objects.filter(conference__id=conference_id)
        auditors = models.ConferenceAuditor.objects.filter(conference__id=conference_id)
        reviews = models.Review.objects.filter(conference__id=conference_id)
        is_speaker = request.user in [obj.speaker.user for obj in speakers]
        is_auditor = request.user in [obj.auditor.user for obj in auditors]
        context = {'object': object,
                   'speakers': speakers,
                   'reviews': reviews,
                   'auditors': auditors,
                   'is_speaker': is_speaker,
                   'is_auditor': is_auditor}
        return render(request, 'static/templates/conference/conference_detail.html', context=context)

class ConferenceCreate(edit.CreateView):
    def get(self, request, **kwargs):
        context = {'form': forms.ConferenceRegisterForm}
        return render(request, 'static/templates/conference/conference_create.html', context)
    
    @transaction.atomic
    def post(self, request, **kwargs):
        context = {}
        form = forms.ConferenceRegisterForm(request.POST or None)
        context['form'] = form
        if not form.is_valid():
            return render(request, 'static/templates/conference/conference_create.html', context)
        
        user_id = request.user.id
        creator = models.Participant.objects.filter(user__id=user_id)[0]
        models.Conference.objects.create(
            name = form.cleaned_data['name'],
            creator = creator,
            description = form.cleaned_data['description'],
            participate_conditionals = form.cleaned_data['participate_conditionals'],
            location = form.cleaned_data['location'],
            date_of_start = form.cleaned_data['date_of_start'],
            date_of_finish = form.cleaned_data['date_of_finish']
        )

        return redirect('/conference/')

class ConferenceUpdate(edit.UpdateView):
    model = models.Conference
    fields = ['name', 'description', 'participate_conditionals', 'location', 'date_of_start', 'date_of_finish']
    template_name = 'static/templates/conference/conference_update.html'
    success_url = '/conference/'

class ConferenceDelete(edit.DeleteView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_delete.html'
    success_url = '/conference/'

class ConferenceAuditor(View):
    
    @transaction.atomic
    def post(self, request, **kwargs):
        context = {}
        conference_id = kwargs['pk']
        user_id = request.user.id
        conference = models.Conference.objects.filter(id=conference_id)[0]
        auditor = models.Participant.objects.filter(user__id=user_id)[0]

        models.ConferenceAuditor.objects.create(
            conference = conference,
            auditor = auditor
        )

        return redirect(f'/conference/{conference_id}/')
