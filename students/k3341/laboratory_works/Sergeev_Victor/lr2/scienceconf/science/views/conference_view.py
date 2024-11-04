from django.views.generic import list, detail, edit
from django.shortcuts import render
from science import models

class ConferenceList(list.ListView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_list.html'

class ConferenceDetail(detail.DetailView):
    model = models.Conference
    def get(self, request, **kwargs):
        object = self.get_object()
        conference_id = kwargs['pk']
        speakers = models.ConferencePerformance.objects.filter(conference__id=conference_id)
        reviews = models.Review.objects.filter(conference__id=conference_id)
        context = {'object': object, 'speakers': speakers, 'reviews': reviews}
        return render(request, 'static/templates/conference/conference_detail.html', context=context)

class ConferenceCreate(edit.CreateView):
    model = models.Conference
    fields = ['name', 'description', 'participate_conditionals', 'location', 'date_of_start', 'date_of_finish']
    template_name = 'static/templates/conference/conference_create.html'
    success_url = '/conference/'

class ConferenceUpdate(edit.UpdateView):
    model = models.Conference
    fields = ['name', 'description', 'participate_conditionals', 'location', 'date_of_start', 'date_of_finish']
    template_name = 'static/templates/conference/conference_update.html'
    success_url = '/conference/'

class ConferenceDelete(edit.DeleteView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_delete.html'
    success_url = '/conference/'
