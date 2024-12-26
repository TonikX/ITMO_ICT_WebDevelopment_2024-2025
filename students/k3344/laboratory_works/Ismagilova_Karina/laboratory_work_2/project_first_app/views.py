from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.contrib.auth import get_user_model
from .forms import AuthentificationCustomForm, NewUserForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Conference, Participant
from .forms import ReviewForm


User = get_user_model()
class UserRegistrationView(CreateView):
    form_class = NewUserForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

class LoginView(View):
    form_class = AuthentificationCustomForm
    template_name = 'login.html'
    success_url = reverse_lazy('login')

class MainView(TemplateView):
    template_name = 'main.html'


class ConferenceListView(ListView):
    model = Conference
    template_name = 'conference_list.html'
    context_object_name = 'conferences'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Conference.objects.all()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(themes__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query'] = query_params.urlencode()
        return context

class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conference_detail.html'
    context_object_name = 'conference'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Зарегистрируйтесь для просмотра деталей конференции!")
            return redirect(reverse('conference_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conference = self.get_object()
        context['reviews'] = conference.review_set.select_related('user').all()
        context['review_form'] = ReviewForm()
        context['is_author'] = self.request.user.is_staff
        return context

    def post(self, request):
        conference = self.get_object()
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.date = conference.start_date
            review.save()
            messages.success(request, "Ваш отзыв успешно добавлен!")
            return redirect('conference_detail', pk=conference.pk)
        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)

class ParticipantRegistrationView(View):
    def post(self, request, pk):
        conference = get_object_or_404(Conference, pk=pk)
        if Participant.objects.filter(user=request.user, conference=conference).exists():
            messages.error(request, "Вы уже зарегистрированы на данную конференцию как участник.")
        else:
            Participant.objects.create(user=request.user, conference=conference, is_author=False)
            request.session['is_author'] = False
            messages.success(request, "Вы успешно зарегистрированы как участник!")
        return redirect('conference_list')

class AuthorRegistrationView(View):
    def post(self, request, pk):
        conference = get_object_or_404(Conference, pk=pk)
        if Participant.objects.filter(user=request.user, conference=conference).exists():
            messages.error(request, "Вы уже зарегистрированы на данную конференцию как автор.")
        else:
            Participant.objects.create(user=request.user, conference=conference, is_author=True)
            request.session['is_author'] = True
            messages.success(request, "Вы успешно зарегистрированы как автор!")
        return redirect('conference_list')

class AllParticipantsListView(ListView):
    model = Conference
    template_name = 'all_participants_list.html'
    context_object_name = 'conferences'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participants = Participant.objects.select_related('user', 'conference').all()
        participant_data = [
            {
                'conference': participant.conference.title,
                'date': participant.conference.start_date,
                'first_name': participant.user.first_name,
                'last_name': participant.user.last_name
            }
            for participant in participants
        ]
        context['participants'] = participant_data
        return context

class UserDashboardView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = 'user_cabinet.html'
    context_object_name = 'user_participants'

    def get_queryset(self):
        return Participant.objects.filter(user=self.request.user).select_related('conference')

    def post(self, request):
        participant_id = request.POST.get("participant_id")
        participant = Participant.objects.filter(id=participant_id, user=request.user).first()
        if participant:
            participant.delete()
            messages.success(request, "Регистрация успешно удалена.")
        else:
            messages.error(request, "Регистрация не найдена или у вас нет прав для её удаления.")
        return redirect('user_dashboard')
