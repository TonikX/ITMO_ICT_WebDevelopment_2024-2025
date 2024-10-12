from django.contrib import admin
from django.urls import path

from .views.account import (RegisterStudentView,
                           LoginStudentView,
                           LogoutAccountView,
                           StudentView)

from .views.navigation import (RootView,
                               AboutView)

from .views.tasks import TasksRoot, TaskIdView

urlpatterns = [
    path('', RootView.as_view(), name='root'),

    # account
    path('account/', StudentView.as_view(), name='account'),
    path('account/register/', RegisterStudentView.as_view(), name='register'),
    path('account/login/', LoginStudentView.as_view(), name='login'),
    path('account/logout/', LogoutAccountView.as_view(), name='logout'),
    # TODO account/settings/

    # tasks
    path('tasks/', TasksRoot.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskIdView.as_view(), name='taskid'),

    # grades

    # other
    path('about/', AboutView.as_view(), name='about'),
    path("admin/", admin.site.urls),
]
