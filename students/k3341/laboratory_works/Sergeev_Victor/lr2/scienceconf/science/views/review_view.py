from django.views.generic import detail, edit
from django.shortcuts import render
from science import models

class ReviewDetail(detail.DetailView):
    model = models.Review
    def get(self, request, **kwargs):
        object = self.get_object()
        review_id = kwargs['pk']
        comments = models.Commentary.objects.filter(review__id=review_id)
        context ={'object': object, 'comments': comments}
        return render(request, 'static/templates/review/review_detail.html', context)

class ReviewCreate(edit.CreateView):
    pass

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
    def get_success_url(self):
        object = self.get_object()
        return f'/conference/{object.conference.id}/'
    
    fields = ['grade', 'description']
    template_name = 'static/templates/review/review_update.html'
