from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from hotels.models import Room
from .forms import ReviewForm

@login_required
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()
            return redirect('room_detail', pk=room_id)
    else:
      form = ReviewForm()
    return redirect('room_detail', pk=room_id)