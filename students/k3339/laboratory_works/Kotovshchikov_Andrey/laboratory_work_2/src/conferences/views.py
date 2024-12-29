from django import views
from django.contrib.auth import mixins
from django.core.exceptions import BadRequest, ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import messages
from conferences.forms import (
    ConferenceRegistrationForm,
    ConferenceUpdatingForm,
    FeedbackForm,
)
from conferences.models import Booking, Conference, Feedback


class ConferenceListView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "conferences/conference-list.html"
    context_object_name = "conferences"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список конференций"
        return context

    def get_queryset(self):
        return Conference.objects.select_related("author").all().order_by("name")


class ConferenceDetailView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Conference
    form_class = ConferenceUpdatingForm
    template_name = "conferences/conference-detail.html"
    pk_url_kwarg = "conference_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        context["is_user_member"] = self.object.members.contains(self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy("conference-detail", kwargs={"conference_pk": self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(
            Conference.objects.select_related("author")
            .select_related("booking")
            .select_related("booking__room")
            .prefetch_related("members"),
            id=self.kwargs[self.pk_url_kwarg],
        )

    def form_valid(self, form):
        if self.object.author.pk != self.request.user.pk:
            raise PermissionDenied()

        return super().form_valid(form)


class ConferenceRegistrationView(mixins.LoginRequiredMixin, views.View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {
            "form": ConferenceRegistrationForm(),
            "title": "Регистрация конференции",
            "action": "Зарегистрировать конференцию",
        }

        return render(request, "conferences/registration-form.html", context)

    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Регистрация конференции",
            "action": "Зарегистрировать конференцию",
        }

        form = ConferenceRegistrationForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "conferences/registration-form.html", context)

        booking_id = form.cleaned_data["booking"].id
        booking = Booking.objects.select_for_update(no_key=True).get(id=booking_id)
        if booking.conference is not None:
            context["message"] = "Выбранная бронь уже занята другим пользователем"
            return render(request, "conferences/registration-form.html", context)

        conference: Conference = form.save(commit=False)
        conference.author = request.user
        conference.save()

        booking.conference = conference
        booking.save()

        context["message"] = "Конференция зарегистрирована"
        context["form"] = ConferenceRegistrationForm()
        return render(request, "conferences/registration-form.html", context)


class ConferenceDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = Conference
    pk_url_kwarg = "conference_pk"
    success_url = reverse_lazy("conference-list")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        conference = get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])
        if conference.author.pk != request.user.pk:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class FeedbackView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Feedback
    form_class = FeedbackForm

    def form_valid(self, form):
        conference = Conference.objects.filter(id=self.kwargs["conference_pk"]).first()
        if conference is None:
            raise ObjectDoesNotExist()

        is_user_member = conference.members.contains(self.request.user)
        if not is_user_member:
            raise PermissionDenied()

        if not conference.is_over():
            raise BadRequest("Конференция еще не окончена")

        feedback: Feedback = form.save(commit=False)
        feedback.author = self.request.user
        feedback.conference = conference
        feedback.save()

        redirect_url = reverse(
            "conference-detail",
            kwargs={"conference_pk": self.kwargs["conference_pk"]},
        )

        return redirect(redirect_url)


class MemberInvitationView(views.View):
    def post(self, request: HttpRequest, *args, **kwargs):
        member_email = request.POST.get("email")
        if member_email is None:
            raise BadRequest("Пустой email адрес")

        redirect_url = reverse(
            "conference-detail",
            kwargs={"conference_pk": kwargs["conference_pk"]},
        )

        conference = get_object_or_404(Conference, pk=kwargs["conference_pk"])
        if conference.author.pk != request.user.pk:
            raise PermissionDenied()

        if conference.is_started():
            raise BadRequest("Конференция началась")

        is_member_exists = conference.members.filter(email=member_email).exists()
        if is_member_exists:
            messages.error(request, "Участник уже добавлен")
            return redirect(redirect_url)

        member = get_user_model().objects.filter(email=member_email).first()
        if member is None:
            messages.error(request, "Участник не найден")
            return redirect(redirect_url)

        conference.members.add(member)
        return redirect(redirect_url)
