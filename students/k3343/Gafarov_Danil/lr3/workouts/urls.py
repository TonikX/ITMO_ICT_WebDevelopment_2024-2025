from django.contrib import admin
from django.urls import path, include

from workouts.views import IndexView, ListCreateWorkouts, WorkoutDetailView, MarkWorkoutDoneApiView, \
    MarkWorkoutFavoriteApiView, RandomWorkoutView, CommentDetailView, CommentListView, RoutineListView, \
    RoutineDetailView, AccountView, AccountDoneWorkoutView, AccountFavoriteWorkoutView, AccountCommentsView, canEdit, \
    AccountPosts

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('workouts/', ListCreateWorkouts.as_view(), name='workouts-list'),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view(), name='workouts-detail'),
    path('workouts/<int:pk>/canEdit/', canEdit.as_view(), name='workouts-list'),
    path('workouts/<int:pk>/done/', MarkWorkoutDoneApiView.as_view(), name='workouts-done'),
    path('workouts/<int:pk>/favorite/', MarkWorkoutFavoriteApiView.as_view(), name='workouts-favorite'),
    path('workouts/random/', RandomWorkoutView.as_view(), name='workouts-random'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comments-detail'),
    path('comment/workout_comment/<int:pk>/', CommentListView.as_view(), name='comments-workout'),

    path('routines/', RoutineListView.as_view(), name='routine-list'),
    path('routines/<int:pk>/', RoutineDetailView.as_view(), name='routine-detail'),

    path('account/', AccountView.as_view(), name='account'),
    path('account/done/', AccountDoneWorkoutView.as_view(), name='account-done'),
    path('account/favorites/', AccountFavoriteWorkoutView.as_view(), name='account-favorite'),
    path('account/comments/', AccountCommentsView.as_view(), name='account-comments'),
    path('account/posts/', AccountPosts.as_view(), name='account-posts'),

    path("admin/", admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
