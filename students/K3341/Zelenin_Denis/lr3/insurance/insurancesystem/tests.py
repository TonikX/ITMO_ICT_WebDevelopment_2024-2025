import ast
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import (
    InsuranceAgent,
    Organization,
    Employee,
    CollectiveContract,
    InsuranceCase,
)


class InsuranceIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Denis",
            password="toor1234"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.agent = InsuranceAgent.objects.create(
            full_name="Alice Smith",
            passport_details="AA111222",
            contact_details="alice@example.com",
        )

    def test_agent_creation_creates_employment_contract(self):
        payload = {
            "full_name": "Bob Stone",
            "passport_details": "BB333444",
            "contact_details": "bob@example.com",
        }

        response = self.client.post(reverse("insuranceagent-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        agent_passport = response.data["agent"]["passport_details"]
        if isinstance(agent_passport, list):
            agent_passport = agent_passport[0]
        elif isinstance(agent_passport, str) and agent_passport.startswith('['):
            try:
                agent_passport = ast.literal_eval(agent_passport)[0]
            except (ValueError, SyntaxError):
                pass
        self.assertEqual(str(agent_passport), payload["passport_details"])
        
        self.assertIn("contract", response.data)
        contract_passport = response.data["contract"]["insurance_agent"]["passport_details"]
        if isinstance(contract_passport, list):
            contract_passport = contract_passport[0]
        elif isinstance(contract_passport, str) and contract_passport.startswith('['):
            try:
                contract_passport = ast.literal_eval(contract_passport)[0]
            except (ValueError, SyntaxError):
                pass
        self.assertEqual(str(contract_passport), payload["passport_details"])

    def test_agent_creation_idempotent_by_passport(self):
        payload = {
            "full_name": self.agent.full_name,
            "passport_details": self.agent.passport_details,
            "contact_details": self.agent.contact_details,
        }

        response = self.client.post(reverse("insuranceagent-list"), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Agent already exists. New contract created.")
        self.assertEqual(InsuranceAgent.objects.filter(passport_details=self.agent.passport_details).count(), 1)

    def test_related_organizations_returns_same_agent_peers(self):
        org_a = Organization.objects.create(
            code="ORG-A",
            full_name="Organization Alpha",
            short_name="Alpha",
            address="City A",
            bank_details="Bank A",
            specialization="Tech",
        )
        org_b = Organization.objects.create(
            code="ORG-B",
            full_name="Organization Beta",
            short_name="Beta",
            address="City B",
            bank_details="Bank B",
            specialization="Health",
        )
        CollectiveContract.objects.create(
            organization=org_a,
            type="collective",
            insurance_agent=self.agent,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            total_payout=1000,
        )
        CollectiveContract.objects.create(
            organization=org_b,
            type="collective",
            insurance_agent=self.agent,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            total_payout=2000,
        )

        url = reverse("organization-related-organizations", args=[org_a.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "ORG-B")

    def test_agent_contracts_count_filters_by_dates(self):
        other_agent = InsuranceAgent.objects.create(
            full_name="Carl Green",
            passport_details="CC555666",
            contact_details="carl@example.com",
        )
        org = Organization.objects.create(
            code="ORG-C",
            full_name="Organization Gamma",
            short_name="Gamma",
            address="City C",
            bank_details="Bank C",
            specialization="Finance",
        )
        CollectiveContract.objects.create(
            organization=org,
            type="collective",
            insurance_agent=self.agent,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            total_payout=3000,
        )
        CollectiveContract.objects.create(
            organization=org,
            type="collective",
            insurance_agent=other_agent,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            total_payout=4000,
        )

        url = reverse("collectivecontract-agent-contracts-count")
        response = self.client.get(url, {"start_date": "2024-01-01", "end_date": "2024-12-31"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["insurance_agent__full_name"], self.agent.full_name)
        self.assertEqual(response.data[0]["collective_count"], 1)
        self.assertEqual(response.data[0]["individual_count"], 0)

    def test_total_payouts_returns_sum_by_contract_type(self):
        org = Organization.objects.create(
            code="ORG-D",
            full_name="Organization Delta",
            short_name="Delta",
            address="City D",
            bank_details="Bank D",
            specialization="Retail",
        )
        contract = CollectiveContract.objects.create(
            organization=org,
            type="collective",
            insurance_agent=self.agent,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            total_payout=5000,
        )
        employee = Employee.objects.create(full_name="Eve Blue", age=30, risk_category="B")
        contract.employees.add(employee)
        InsuranceCase.objects.create(
            contract=contract,
            date=date.today(),
            reason="Accident",
            decision=True,
            payout_amount=1500,
            emp=employee,
        )
        InsuranceCase.objects.create(
            contract=contract,
            date=date.today(),
            reason="Accident 2",
            decision=True,
            payout_amount=500,
            emp=employee,
        )

        url = reverse("insurancecase-total-payouts")
        response = self.client.get(url, {"start_date": now().date().isoformat(), "end_date": now().date().isoformat()})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["contract__type"], "collective")
        total_payout = response.data[0]["total_payout"]
        if isinstance(total_payout, Decimal):
            self.assertEqual(total_payout, Decimal("2000"))
        else:
            self.assertEqual(str(total_payout), "2000")

