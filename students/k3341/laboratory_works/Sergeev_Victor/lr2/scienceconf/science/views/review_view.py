from django.views.generic import detail, edit
from django.views import View
from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from science import models, forms

class ReviewDetail(detail.DetailView):
    model = models.Review
    def get(self, request, **kwargs):
        object = self.get_object()
        review_id = kwargs['pk']
        comments = models.Commentary.objects.filter(review__id=review_id)
        context ={'object': object, 'comments': comments}
        return render(request, 'static/templates/review/review_detail.html', context)

class ReviewCreate(View):
    def get(self, request, **kwargs):
        context = {'form': forms.ReviewForm}
        return render(request, 'static/templates/review/review_create.html', context)
    
    @transaction.atomic
    def post(self, request, **kwargs):
        form = forms.ReviewForm(request.POST or None)
        context = {'form': form}

        if not form.is_valid():
            return render(request, 'static/templates/review/review_create.html', context)
        grade = form.cleaned_data['grade']

        if grade > 10 or grade < 0:
            context['message'] = 'Invalid grade value'
            return render(request, 'static/templates/review/review_create.html', context)
        
        conference_id = kwargs['conf_pk']
        user_id = request.user.id
        conference = models.Conference.objects.filter(id=conference_id)[0]
        author = models.Participant.objects.filter(user__id=user_id)[0]

        models.Review.objects.create(
            grade = grade,
            description = form.cleaned_data['description'],
            conference = conference,
            author = author
        )

        return redirect(f'/conference/{conference_id}/')

class ReviewDelete(edit.DeleteView):
    model = models.Review
    def get_success_url(self):
        object = self.get_object()
        return f'/conference/{object.conference.id}'

    def get(self, request, **kwargs):
        object = self.get_object()
        context = {'object': object}
        return render(request, 'static/templates/review/review_delete.html', context)
        
class ReviewUpdate(edit.UpdateView):
    model = models.Review
    fields = ['grade', 'description']
    template_name = 'static/templates/review/review_update.html'
    def get(self, request, **kwargs):
        context = {'form': forms.ReviewForm}
        return render(request, 'static/templates/review/review_update.html', context)

    @transaction.atomic
    def post(self, request, **kwargs):
        context = {}
        form = forms.ReviewForm(request.POST or None)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'static/templates/review/review_update.html')
        
        grade = form.cleaned_data['grade']
        if grade > 10 or grade < 0:
            context['message'] = 'Invalid grade value'
            return render(request, 'static/templates/review/review_create.html', context)
        
        conference_id = kwargs['conf_pk']
        review_id = kwargs['pk']
        models.Review.objects.filter(id=review_id).update(
            grade = grade,
            description = form.cleaned_data['description'],
            date = timezone.now()
        )

        return redirect(f'/conference/{conference_id}/review/{review_id}/')
