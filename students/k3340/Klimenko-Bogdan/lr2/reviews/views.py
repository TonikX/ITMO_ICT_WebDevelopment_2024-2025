from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room_id = self.kwargs['room_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bookings:room_detail', kwargs={'pk': self.kwargs['room_id']})