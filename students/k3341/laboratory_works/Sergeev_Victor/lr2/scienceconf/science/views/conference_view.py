from django.views.generic import list, detail, edit
from science import models

class ConferenceList(list.ListView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_list.html'

class ConferenceDetail(detail.DetailView):
    model = models.Conference
    template_name = 'static/templates/conference/conference_detail.html'

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
