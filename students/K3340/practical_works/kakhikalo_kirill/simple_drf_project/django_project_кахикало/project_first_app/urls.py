from django.urls import path
from . import views
from .views import AutoRetrieveView, AutoUpdateView, AutoCreateView, AutoDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.detail),
    path('owner/', views.list_view),
    path('auto/<int:pk>/', AutoRetrieveView.as_view()),
    path('auto/list/', views.AutoListView.as_view()),
    path('auto/<int:pk>/update/', AutoUpdateView.as_view()),
    path('auto/create/', AutoCreateView.as_view()),
    path('auto/<int:pk>/delete/', AutoDeleteView.as_view()),
    path('owner/create/', views.create_view),
]
