from django.views.generic import edit
from django.views import View
from django.shortcuts import redirect
from django.utils import timezone
from science import models, forms

class CommentCreate(View):
    def post(self, request, **kwargs):
        context = {}
        form = forms.CommentForm(request.POST or None)
        context['form'] = form
        review_id = kwargs['rev_pk']
        conf_id = kwargs['conf_pk']
        user_id = request.user.id
        if form.is_valid():
            form = form.save(commit=False)
            form.review_id = review_id
            form.author = models.Participant.objects.get(user__id=user_id)
            form.date = timezone.now()
            form.save()
        return redirect(f'/conference/{conf_id}/review/{review_id}/')

class CommentUpdate(View):
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
