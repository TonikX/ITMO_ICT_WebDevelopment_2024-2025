from django.urls import path
from . import views

app_name = "peer_review_app"

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),

    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/details/', views.TaskDetailWithRelationsView.as_view(), name='task-detail-with-relations'),

    path('criteria/', views.CriterionListCreateView.as_view(), name='criterion-list-create'),
    path('criteria/<int:pk>/', views.CriterionDetailView.as_view(), name='criterion-detail'),

    path('options/', views.OptionListCreateView.as_view(), name='option-list-create'),
    path('options/<int:pk>/', views.OptionDetailView.as_view(), name='option-detail'),

    path('submissions/', views.SubmissionListCreateView.as_view(), name='submission-list-create'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),

    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    path('statistics/', views.TaskStatisticsView.as_view(), name='task-statistics'),
    path('tasks/<int:task_id>/average-score/', views.AverageScoreView.as_view(), name='average-score'),

]
