from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, ListView, CreateView

from reviews.forms import ReviewForm
from reviews.models import Review
from tours.models import Departure


# Create your views here.
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'

    def get_queryset(self):
        return (Review.objects
                .filter(author=self.request.user)
                .select_related('departure__tour')
                .order_by('-created_at'))


class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'add_review.html'

    def dispatch(self, request, *args, **kwargs):
        self.departure = get_object_or_404(Departure, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.departure = self.departure
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departure'] = self.departure
        return ctx

    def get_success_url(self):
        return reverse('tours:detail', kwargs={'pk': self.departure.tour.pk})