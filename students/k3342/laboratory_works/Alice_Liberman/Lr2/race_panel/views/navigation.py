from django.views.generic import TemplateView

from race_panel.models import Racer


class RootView(TemplateView):
    template_name = 'root.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.session.get("user_id", None)
        try:
            user_model = Racer.objects.get(id=user)
            context.update(
                {
                    'context_insert': 'inserts/root_login.html',
                    'userinfo': user_model
                }
            )
        except Racer.DoesNotExist:
            context.update({'context_insert': 'inserts/root_not_logged_in.html'})

        return context


class AboutView(TemplateView):
    template_name = 'about.html'
