from django.views.generic import TemplateView

from ..forms import SignInStudentForm
from ..models import Student


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if user_id := self.request.session.get('user_id'):
            context['student'] = Student.objects.get(pk=user_id)

        return context