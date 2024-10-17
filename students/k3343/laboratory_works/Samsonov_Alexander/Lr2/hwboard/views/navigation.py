from django.views.generic import TemplateView

from ..forms import LoginStudentForm
from ..models import Student


class RootView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_contents'] = 'root.html'
        context['title'] = 'Homepage'

        if user_id := self.request.session.get('user_id'):
            context['student'] = Student.objects.get(pk=user_id)
            context['account'] = 'account/account_info.html'

        else:
            context['account'] = 'account/login_form.html'
            context['form'] = LoginStudentForm()

        return context


class AboutView(RootView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_contents'] = 'about.html'
        context['title'] = 'About'

        return context
