from django.urls import path
from . import views

urlpatterns = [
    path('guest/<str:username>/', views.guest_detail, name='guest_detail'),  # Используем <str:username>
    path('guests/', views.guest_list, name='guest_list'),  # URL для списка гостей
    path('rooms/', views.RoomListView.as_view(), name='room_list'),  # URL для списка номеров
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),  # URL для просмотра номера по ID
    path('rooms/<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),  # URL для обновления номера
    path('guests/create/', views.create_guest, name='create_guest'),  # Создание гостя
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),  # Создание номера
    path('rooms/<int:pk>/update/', views.RoomUpdateView.as_view(), name='room_update'),  # Обновление номера
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),  # Удаление номера
    path('register/', views.register, name='register'),  # URL для регистрации
]
