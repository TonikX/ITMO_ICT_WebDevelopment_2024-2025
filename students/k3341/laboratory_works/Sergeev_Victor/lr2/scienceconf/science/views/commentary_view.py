from django.http import HttpResponseForbidden
from django.views import View
from django.shortcuts import redirect
from django.utils import timezone
from science import models, forms

class CommentCreate(View):
    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Sign in to be able see this page")
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
