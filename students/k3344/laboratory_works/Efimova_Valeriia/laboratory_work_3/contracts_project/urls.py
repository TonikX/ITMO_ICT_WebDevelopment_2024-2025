"""
URL configuration for contracts_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import contracts_app.views as views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("agents/", views.AgentListCreateAPIView.as_view(), name="agents"),
    path("agents/<int:pk>/", views.AgentDetailAPIView.as_view(), name="agent-detail"),
    path(
        "organizations/",
        views.OrganizationListCreateAPIView.as_view(),
        name="organizations",
    ),
    path(
        "organizations/<int:pk>/",
        views.OrganizationDetailAPIView.as_view(),
        name="organization-detail",
    ),
    path("employees/", views.EmployeeListCreateAPIView.as_view(), name="employees"),
    path(
        "employees/<int:pk>/",
        views.EmployeeDetailAPIView.as_view(),
        name="employee-detail",
    ),
    path("contracts/", views.ContractListCreateAPIView.as_view(), name="contracts"),
    path(
        "contracts/<int:pk>/",
        views.ContractDetailAPIView.as_view(),
        name="contract-detail",
    ),
    path(
        "insurance_cases/",
        views.InsuranceCaseListCreateAPIView.as_view(),
        name="insurance_cases",
    ),
    path(
        "insurance_cases/<int:pk>/",
        views.InsuranceCaseDetailAPIView.as_view(),
        name="insurance_case-detail",
    ),
    path(
        "employment_contracts/",
        views.EmploymentContractListCreateAPIView.as_view(),
        name="employment_contracts",
    ),
    path(
        "employment_contracts/<int:pk>/",
        views.EmploymentContractDetailAPIView.as_view(),
        name="employment_contract-detail",
    ),
    path(
        "contracts/report/<int:pk>/",
        views.ContractReportView.as_view(),
        name="contract-report",
    ),
]
