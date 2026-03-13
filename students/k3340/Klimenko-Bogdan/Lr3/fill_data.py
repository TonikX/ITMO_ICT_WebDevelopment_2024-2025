import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import (
    Habitat, Department, Building, Enclosure, Staff, Animal,
    FeedingRationType, FeedingRation, Zoo, WinteringPlace,
    FeedingHistory, CaretakerAssignment, VeterinarianAssignment,
    TransferHistory
)
from django.db import models  # для аннотаций в итоге

def clear_data():
    """Очистка всех таблиц (порядок важен из-за внешних ключей)"""
    TransferHistory.objects.all().delete()
    CaretakerAssignment.objects.all().delete()
    VeterinarianAssignment.objects.all().delete()
    FeedingHistory.objects.all().delete()
    Animal.objects.all().delete()
    Staff.objects.all().delete()
    Enclosure.objects.all().delete()
    Building.objects.all().delete()
    Department.objects.all().delete()
    Habitat.objects.all().delete()
    FeedingRation.objects.all().delete()
    FeedingRationType.objects.all().delete()
    Zoo.objects.all().delete()
    WinteringPlace.objects.all().delete()
    print("Все старые данные удалены.")

def create_data():
    # ------------------------------------------------------------------
    # 1. Справочники
    # ------------------------------------------------------------------
    ration_type_main = FeedingRationType.objects.create(name="Основной")
    ration_type_diet = FeedingRationType.objects.create(name="Диетический")
    print("Созданы типы рационов.")

    ration_std = FeedingRation.objects.create(
        number="R-001",
        name="Стандартный",
        ration_type=ration_type_main
    )
    ration_light = FeedingRation.objects.create(
        number="R-002",
        name="Лёгкий",
        ration_type=ration_type_diet
    )
    print("Созданы рационы.")

    habitat_savanna = Habitat.objects.create(
        name="Саванна",
        continent="Африка",
        country="Кения",
        description="Открытая местность с высокой травой"
    )
    habitat_forest = Habitat.objects.create(
        name="Лес",
        continent="Евразия",
        country="Россия",
        description="Смешанный лес"
    )
    print("Созданы зоны обитания.")

    zoo_msk = Zoo.objects.create(
        name="Московский зоопарк",
        address="ул. Большая Грузинская, 1",
        contact_phone="+7 (495) 123-45-67",
        contact_email="info@moscowzoo.ru"
    )
    zoo_spb = Zoo.objects.create(
        name="Ленинградский зоопарк",
        address="ул. Ленина, 10",
        contact_phone="+7 (812) 765-43-21",
        contact_email="info@spbzoo.ru"
    )
    print("Созданы зоопарки.")

    winter_egypt = WinteringPlace.objects.create(
        code="EG-01",
        country="Египет",
        name="Оазис Эль-Файюм"
    )
    winter_india = WinteringPlace.objects.create(
        code="IN-02",
        country="Индия",
        name="Национальный парк Канха"
    )
    print("Созданы места зимовки.")

    # ------------------------------------------------------------------
    # 2. Отделы, здания, вольеры
    # ------------------------------------------------------------------
    dept_predators = Department.objects.create(name="Хищники", description="Крупные и мелкие хищники")
    dept_birds = Department.objects.create(name="Птицы", description="Водоплавающие и хищные птицы")
    dept_reptiles = Department.objects.create(name="Рептилии", description="Пресмыкающиеся")
    print("Созданы отделы.")

    building_pred = Building.objects.create(
        name="Павильон хищников",
        building_type="winter",
        department=dept_predators
    )
    building_birds = Building.objects.create(
        name="Птичник",
        building_type="summer",
        department=dept_birds
    )
    building_rept = Building.objects.create(
        name="Террариум",
        building_type="winter",
        department=dept_reptiles
    )
    print("Созданы здания.")

    enc_pred_1 = Enclosure.objects.create(
        number="Х-001",
        department=dept_predators,
        building=building_pred,
        is_communal=False,
        has_pool=False,
        has_equipment=True,
        has_indoor=True,
        capacity=2
    )
    enc_pred_2 = Enclosure.objects.create(
        number="Х-002",
        department=dept_predators,
        building=building_pred,
        is_communal=True,
        has_pool=True,
        has_equipment=True,
        has_indoor=False,
        capacity=4
    )
    enc_birds_1 = Enclosure.objects.create(
        number="П-001",
        department=dept_birds,
        building=building_birds,
        is_communal=False,
        has_pool=True,
        has_equipment=False,
        has_indoor=True,
        capacity=10
    )
    enc_rept_1 = Enclosure.objects.create(
        number="Р-001",
        department=dept_reptiles,
        building=building_rept,
        is_communal=False,
        has_pool=False,
        has_equipment=True,
        has_indoor=True,
        capacity=5
    )
    print("Созданы вольеры.")

    # ------------------------------------------------------------------
    # 3. Сотрудники
    # ------------------------------------------------------------------
    caretaker1 = Staff.objects.create(
        personnel_number="СМ-001",
        full_name="Иванов Иван Иванович",
        birth_date="1985-03-15",
        phone="+7 (999) 123-45-67",
        email="ivanov@zoo.ru",
        staff_type="caretaker"
    )
    caretaker2 = Staff.objects.create(
        personnel_number="СМ-002",
        full_name="Петрова Анна Сергеевна",
        birth_date="1990-07-22",
        phone="+7 (999) 765-43-21",
        email="petrova@zoo.ru",
        staff_type="caretaker"
    )
    vet1 = Staff.objects.create(
        personnel_number="ВЕТ-001",
        full_name="Сидоров Алексей Викторович",
        birth_date="1978-11-02",
        phone="+7 (999) 555-66-77",
        email="sidorov@zoo.ru",
        staff_type="vet"
    )
    vet2 = Staff.objects.create(
        personnel_number="ВЕТ-002",
        full_name="Кузнецова Елена Дмитриевна",
        birth_date="1982-09-10",
        phone="+7 (999) 444-33-22",
        email="kuznetsova@zoo.ru",
        staff_type="vet"
    )
    print("Созданы сотрудники.")

    # ------------------------------------------------------------------
    # 4. Животные
    # ------------------------------------------------------------------
    lion = Animal.objects.create(
        unique_number="AN-001",
        name="Лео",
        birth_date="2018-06-10",
        gender="M",
        animal_type="mammal",
        habitat=habitat_savanna,
        department=dept_predators,
        current_enclosure=enc_pred_1,
        ownership_type="own",
        purchase_date="2019-09-01",
        seller_organization="Африка сафари",
        arrival_date="2019-09-01"
    )

    tiger = Animal.objects.create(
        unique_number="AN-002",
        name="Шерхан",
        birth_date="2017-03-20",
        gender="M",
        animal_type="mammal",
        habitat=habitat_savanna,
        department=dept_predators,
        current_enclosure=enc_pred_2,
        ownership_type="own",
        purchase_date="2018-05-10",
        seller_organization="Индийский зоопарк",
        arrival_date="2018-05-10"
    )

    leopard = Animal.objects.create(
        unique_number="AN-003",
        name="Багира",
        birth_date="2019-11-05",
        gender="F",
        animal_type="mammal",
        habitat=habitat_forest,
        department=dept_predators,
        current_enclosure=enc_pred_2,
        ownership_type="own",
        purchase_date="2020-02-20",
        seller_organization="Частный заводчик",
        arrival_date="2020-02-20"
    )

    eagle = Animal.objects.create(
        unique_number="AN-004",
        name="Орлик",
        birth_date="2020-04-15",
        gender="M",
        animal_type="bird",
        habitat=habitat_forest,
        department=dept_birds,
        current_enclosure=enc_birds_1,
        wintering_place=winter_india,
        departure_date="2023-10-01",
        return_date="2024-03-15",  # исправлено
        ownership_type="own",
        purchase_date="2021-06-01",
        seller_organization="Питомник птиц",
        arrival_date="2021-06-01"
    )

    snake = Animal.objects.create(
        unique_number="AN-005",
        name="Каа",
        birth_date="2022-01-10",
        gender="M",
        animal_type="reptile",
        habitat=habitat_forest,
        department=dept_reptiles,
        current_enclosure=enc_rept_1,
        normal_temperature=28.5,
        hibernation_start="2024-11-01",
        hibernation_end="2025-03-01",
        ownership_type="lease",
        owner_zoo=zoo_msk,
        lease_start="2023-01-01",
        lease_end="2024-12-31",
        lease_cost=50000.00,
        arrival_date="2023-01-01"
    )

    turtle = Animal.objects.create(
        unique_number="AN-006",
        name="Тортилла",
        birth_date="2015-05-20",
        gender="F",
        animal_type="reptile",
        habitat=habitat_forest,
        department=dept_reptiles,
        current_enclosure=enc_rept_1,
        normal_temperature=26.0,
        hibernation_start="2024-10-15",
        hibernation_end="2025-04-15",
        ownership_type="lease",
        owner_zoo=zoo_spb,
        lease_start="2024-01-01",
        lease_end="2024-12-31",
        lease_cost=30000.00,
        arrival_date="2024-01-01"
    )
    print("Созданы животные.")

    # ------------------------------------------------------------------
    # 5. Назначения (рационы, смотрители, ветеринары, истории)
    # ------------------------------------------------------------------
    FeedingHistory.objects.create(
        animal=lion,
        ration=ration_std,
        start_date="2024-01-01",
        end_date=None
    )
    FeedingHistory.objects.create(
        animal=tiger,
        ration=ration_std,
        start_date="2024-02-01",
        end_date=None
    )
    FeedingHistory.objects.create(
        animal=eagle,
        ration=ration_light,
        start_date="2024-03-01",
        end_date=None
    )
    print("Созданы истории кормления.")

    CaretakerAssignment.objects.create(
        caretaker=caretaker1,
        animal=lion,
        start_date="2024-01-01",
        end_date=None
    )
    CaretakerAssignment.objects.create(
        caretaker=caretaker1,
        animal=tiger,
        start_date="2024-01-01",
        end_date=None
    )
    CaretakerAssignment.objects.create(
        caretaker=caretaker2,
        animal=eagle,
        start_date="2024-02-01",
        end_date=None
    )
    print("Созданы назначения смотрителей.")

    VeterinarianAssignment.objects.create(
        veterinarian=vet1,
        animal=lion,
        start_date="2024-01-01",
        end_date=None
    )
    VeterinarianAssignment.objects.create(
        veterinarian=vet2,
        animal=tiger,
        start_date="2024-01-01",
        end_date=None
    )
    VeterinarianAssignment.objects.create(
        veterinarian=vet1,
        animal=eagle,
        start_date="2024-03-01",
        end_date=None
    )
    print("Созданы назначения ветеринаров.")

    TransferHistory.objects.create(
        animal=lion,
        from_enclosure=enc_pred_1,
        to_enclosure=enc_pred_1,
        transfer_date="2019-09-01 10:00:00"
    )
    TransferHistory.objects.create(
        animal=tiger,
        from_enclosure=enc_pred_1,
        to_enclosure=enc_pred_2,
        transfer_date="2020-05-10 14:30:00"
    )
    TransferHistory.objects.create(
        animal=leopard,
        from_enclosure=enc_pred_1,
        to_enclosure=enc_pred_2,
        transfer_date="2020-06-01 09:15:00"
    )
    print("Созданы истории пересадок.")

    print("\n=== ИТОГОВАЯ ИНФОРМАЦИЯ ===")
    print(f"Всего животных: {Animal.objects.count()}")
    print(f" - в коммунальных вольерах: {Animal.objects.filter(current_enclosure__is_communal=True).count()}")
    print(f" - арендованных: {Animal.objects.filter(ownership_type='lease').count()}")
    print(f"Всего отделов: {Department.objects.count()}")
    print(f"Всего вольеров: {Enclosure.objects.count()}")
    print(f" - пустых: {Enclosure.objects.annotate(animal_count=models.Count('animals')).filter(animal_count=0).count()}")
    print("Скрипт успешно выполнен.")

if __name__ == "__main__":
    clear_data()
    create_data()