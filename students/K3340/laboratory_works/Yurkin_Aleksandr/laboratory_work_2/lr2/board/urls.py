from django.urls import path

from .views.main import MainView
from .views.students import SignUpStudentView, SignInStudentView, LogoutAccountView
from .views.tasks import TasksView



urlpatterns = [
    path('', MainView.as_view(), name='root'),
    path('signup/', SignUpStudentView.as_view(), name='signup'),
    path('signin/', SignInStudentView.as_view(), name='signin'),
    path('logout/', LogoutAccountView.as_view(), name='logout'),
    path('tasks/', TasksView.as_view(), name='tasks_list')
]