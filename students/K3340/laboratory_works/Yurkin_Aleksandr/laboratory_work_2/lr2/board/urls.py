from django.urls import path

from .views.main import MainView
from .views.students import SignUpStudentView, SignInStudentView, LogoutAccountView
from .views.tasks import TasksView, TaskDetailView, AssignmentCreateView
from .views.grades import GradesTableView


urlpatterns = [
    path('', MainView.as_view(), name='root'),
    path('signup/', SignUpStudentView.as_view(), name='signup'),
    path('signin/', SignInStudentView.as_view(), name='signin'),
    path('logout/', LogoutAccountView.as_view(), name='logout'),
    path('tasks/', TasksView.as_view(), name='tasks_list'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task_details'),
    path('tasks/<int:task_id>/create_assignment', AssignmentCreateView.as_view(), name='create_assignment'),
    path('grades', GradesTableView.as_view(), name='grades_table')
]