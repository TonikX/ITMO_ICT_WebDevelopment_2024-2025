from django.urls import path

from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('book_tour/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('sold_tours_by_country/', views.sold_tours_by_country, name='sold_tours_by_country'),
    path('register/', views.register_reviewer, name='register_reviewer'),
    path('register_agency/', views.register_agency, name='register_agency'),
    path('create_tour/', views.create_tour, name='create_tour'),
    path('edit_tour/<int:tour_id>/', views.edit_tour, name='edit_tour'),
    path('agency_dashboard/', views.agency_dashboard, name='agency_dashboard'),
    path('delete_tour/<int:tour_id>/', views.delete_tour, name='delete_tour'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add_review/<int:tour_id>/', views.add_review, name='add_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('login_reviewer/', views.user_login, name='login_reviewer'),
    path('login_agency/', views.user_login, name='login_agency'),
    path('tour_detail/<int:tour_id>/', views.tour_detail, name='tour_detail'),
]
