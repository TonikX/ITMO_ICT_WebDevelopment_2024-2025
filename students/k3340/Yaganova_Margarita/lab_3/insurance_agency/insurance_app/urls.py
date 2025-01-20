from django.urls import path
from .views import *

urlpatterns = [
    path('clients/', ClientListCreateView.as_view()),
    path('clients/<int:id>/', ClientRetrieveUpdateDestroyAPIView.as_view()),
    path('specializations/', SpecializationListCreateAPIView.as_view()),
    path('enterprises/', EnterpriseListCreateAPIView.as_view()),
    path('enterprises/<int:id>/', EnterpriseRetrieveUpdateDestroyAPIView.as_view()),
    path('payouts/', PayoutListCreateAPIView.as_view()),
    path('payouts/<int:id>/', PayoutUpdateDeleteAPIView.as_view()),
    path('agents/', AgentListAPIView.as_view()),
    path('agents/<int:id>/', AgentDeleteAPIView.as_view()),
    path('employee_contracts/', EmployeeContractListCreateAPIView.as_view()),
    path('employee_contracts/<int:id>/', EmployeeContractUpdateDeleteAPIView.as_view()),
    path('contracts/', InsuranceContractListCreateAPIView.as_view()),
    path('contracts/<int:id>/', InsuranceContractUpdateDeleteAPIView.as_view()),
    path('insurance_claims/', InsuranceClaimListCreateAPIView.as_view()),
    path('insurance_claims/<int:id>/', InsuranceClaimUpdateDeleteAPIView.as_view()),
    path('agents/active/', ActiveAgentsListView.as_view()),
    path('contracts/enterprise/<int:id>/', EnterpriseContractsListView.as_view()),
    path('contracts/agent/<int:id>/', AgentContractsListView.as_view()),
    path('insurance_claims/enterprise/<int:id>/', EnterpriseInsuranceClaimsListView.as_view()),
    path('contracts/specialization/<int:id>', SpecializationContractsListView.as_view()),
    path('contracts/client/<int:id>', ClientContractsListView.as_view())
]
