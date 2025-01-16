# from django.urls import path
# from . import views

# urlpatterns = [
#     path('homeworks/', views.homework_list, name='homework_list'),
# ]


# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # 添加前缀 /assignments/
#     path('assignments/', include('assignments.urls')),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('homeworks/', views.homework_list, name='homework_list'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.homework_list, name='homework_list'),
# ]


# from django.urls import path
# from . import views


# urlpatterns = [
#     path('homeworks/', views.homework_list, name='homework_list'),
#     path('register/', views.register, name='register'),
#     path('homeworks/<int:homework_id>/submit/', views.submit_homework, name='submit_homework'),
#     path('grades/', views.grade_table, name='grade_table'),
# ]


from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('homeworks/', views.homework_list, name='homework_list'),
    path('homeworks/<int:homework_id>/', views.homework_detail, name='homework_detail'),
    path('homeworks/<int:homework_id>/submit/', views.submit_homework, name='submit_homework'),
    
    path('grades/', views.grade_table, name='grade_table'),
    path('teachers/', views.teacher_list, name='teacher_list'),

    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


# # assignments/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.homework_list, name='homework_list'),  # 首页显示作业列表
#     path('submit/', views.submit_homework, name='submit_homework'),  # 提交作业页面
# ]
