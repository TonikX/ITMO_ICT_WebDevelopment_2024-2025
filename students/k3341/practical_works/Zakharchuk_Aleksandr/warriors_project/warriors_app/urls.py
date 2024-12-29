from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from warriors_app import views

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hardbeat34@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("warriors/", views.WarriorAPIView.as_view()),
    path("profession/create", views.ProfessionCreateView.as_view()),
    path("skills/", views.SkillView.as_view()),
    path("warriors/list/", views.WarriorListAPIView.as_view()),
    path("profession/generic_create/", views.ProfessionCreateAPIView.as_view()),
    path("warriors/profession/", views.WarriorWithProfessionView.as_view()),
    path("warriors/skill/", views.WarriorWithSkillView.as_view()),
    path("warriors/<int:pk>/", views.WarriorDetailView.as_view()),
    path("warriors/delete/<int:pk>/", views.WarriorDeleteView.as_view()),
    path("warriors/update/<int:pk>/", views.WarriorUpdateView.as_view()),
    path("doc/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("doc/redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
