# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('reserve/<int:flight_id>/', views.reserve, name='reserve'),
#     path('my_reservations/', views.my_reservations, name='my_reservations'),
#     path('add_comment/<int:flight_id>/', views.add_comment, name='add_comment'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),     # 根路径指向首页
    path('reserve/<int:flight_id>/', views.reserve, name='reserve'),    # 航班预定路径
    path('my_reservations/', views.my_reservations, name='my_reservations'),    # 我的预定页面              
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),  # 取消预定的路由
    path('add_comment/<int:flight_id>/', views.add_comment, name='add_comment'),    # 添加评论路径
]
