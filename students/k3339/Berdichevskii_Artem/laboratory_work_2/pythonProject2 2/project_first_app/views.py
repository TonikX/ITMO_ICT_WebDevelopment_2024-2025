from django.contrib import messages
from django.contrib.auth import login, get_user_model, authenticate
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from .models import User, Conference, Review, Participant
from .forms import NewUserForm, ReviewForm, ParticipantForm, ConferenceForm, CustomAuthenticationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Participant


class CustomLoginView(View):
    template_name = 'project_first_app/login.html'
    authentication_form = CustomAuthenticationForm

    def get(self, request):
        form = self.authentication_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.authentication_form(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
        return render(request, self.template_name, {'form': form})


class HomeView(ListView):
    model = Conference
    template_name = 'project_first_app/home.html'
    context_object_name = 'conferences'


class RegisterView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'project_first_app/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class AddReviewView(View):
    template_name = 'project_first_app/add_review.html'

    def get(self, request, conference_id):
        form = ReviewForm()
        conference = get_object_or_404(Conference, pk=conference_id)
        return render(request, self.template_name, {'form': form, 'conference': conference})

    def post(self, request, conference_id):
        form = ReviewForm(request.POST)
        conference = get_object_or_404(Conference, pk=conference_id)

        if form.is_valid():
            review = form.save(commit=False)  # Не сохраняем еще в БД
            review.user = request.user  # Добавляем информацию о комментаторе
            review.conference = conference  # Устанавливаем конференцию
            review.save()  # Теперь сохраняем в БД
            return redirect('conference_detail', pk=conference_id)

        return render(request, self.template_name, {'form': form, 'conference': conference})


class ParticipantListView(ListView):
    model = Participant
    template_name = 'project_first_app/participants.html'
    context_object_name = 'participants'
    paginate_by = 10  # Количество участников на странице

    def get_queryset(self):
        query_user = self.request.GET.get('user')
        query_conference = self.request.GET.get('conference')
        registered = self.request.GET.get('registered', 'false') == 'true'
        queryset = Participant.objects.all()

        if registered:
            queryset = queryset.filter(user__is_active=True)

        if query_user:
            queryset = queryset.filter(user__username__icontains=query_user)
        if query_conference:
            queryset = queryset.filter(conference__title__icontains=query_conference)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['participants'] = page_obj
        context['query_user'] = self.request.GET.get('user', '')
        context['query_conference'] = self.request.GET.get('conference', '')
        context['registered'] = self.request.GET.get('registered', 'false') == 'true'
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return context


class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'project_first_app/conference.html'
    context_object_name = 'conference'


class NewConferenceView(CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'project_first_app/new_conference.html'
    success_url = reverse_lazy('home')


class EditConferenceView(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'project_first_app/edit_conference.html'
    success_url = reverse_lazy('home')


class DeleteConferenceView(DeleteView):
    model = Conference
    template_name = 'project_first_app/delete_conference.html'
    success_url = reverse_lazy('home')


class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'project_first_app/participant_detail.html'
    context_object_name = 'participant'


class ReviewListView(ListView):
    model = Review
    template_name = 'project_first_app/review_list.html'
    context_object_name = 'reviews'


class AuthorRegistrationView(View):
    template_name = 'project_first_app/author_registration.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # перенаправить на страницу входа

        conferences = Conference.objects.all()
        my_participants = Participant.objects.filter(user=request.user)

        return render(request, self.template_name, {
            'conferences': conferences,
            'my_participants': my_participants
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # перенаправить на страницу входа

        conference_id = request.POST.get('conference')
        conference = get_object_or_404(Conference, id=conference_id)

        if Participant.objects.filter(user=request.user, conference=conference).exists():
            messages.error(request, "Вы уже зарегистрированы на эту конференцию.")
        else:
            Participant.objects.create(user=request.user, conference=conference)
            messages.success(request, "Вы успешно зарегистрировались на конференцию.")

        return HttpResponseRedirect(request.path_info)


class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'project_first_app/edit_participant.html'

    def get_success_url(self):
        return reverse_lazy('participant-list')


class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'project_first_app/delete_participant.html'

    def get_success_url(self):
        return reverse_lazy('author-registration')

    def delete(self, request, *args, **kwargs):
        participant = self.get_object()
        if participant.user != request.user:
            return HttpResponseForbidden("Вы не можете удалить эту регистрацию.")
        return super().delete(request, *args, **kwargs)

