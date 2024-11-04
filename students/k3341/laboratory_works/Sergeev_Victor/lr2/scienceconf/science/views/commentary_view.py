from django.views.generic import edit
from science import models

class CommentUpdate(edit.UpdateView):
    model = models.Commentary
    fields = ['description']
    template_name = 'static/templates/commentary/commentary_update.html'
    def get_success_url(self) -> str:
        object = self.get_object()
        return f'/conference/{object.review.conference.id}/review/{object.review.id}'

class CommentDelete(edit.DeleteView):
    model = models.Commentary
    template_name = 'static/templates/commentary/commentary_delete.html'
    def get_success_url(self) -> str:
        object = self.get_object()
        return f'/conference/{object.review.conference.id}/review/{object.review.id}'
