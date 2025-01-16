from django.test import TestCase
from .models import Owner, Car, Ownership


class SimpleTestCase(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(name="Тест", license_date="2015-05-05")
        self.car = Car.objects.create(brand="TestBrand", color="Green")
        self.ownership = Ownership.objects.create(owner=self.owner, car=self.car, ownership_date="2020-01-01")

    def test_owner_creation(self):
        self.assertEqual(self.owner.name, "Тест")

    def test_car_association(self):
        # Проверим, что через ownership владелец имеет связанную машину
        self.assertEqual(self.owner.ownerships.count(), 1)
        self.assertEqual(self.owner.ownerships.first().car.brand, "TestBrand")
