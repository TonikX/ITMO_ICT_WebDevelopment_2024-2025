from django.db import models
from django.contrib.auth.models import User  # для связи с пользователями, если потребуется

# Справочник типов рациона
class FeedingRationType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название типа')

    class Meta:
        verbose_name = 'Тип рациона'
        verbose_name_plural = 'Типы рационов'

    def __str__(self):
        return self.name

# Рацион кормления
class FeedingRation(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер рациона')
    name = models.CharField(max_length=200, verbose_name='Название')
    ration_type = models.ForeignKey(FeedingRationType, on_delete=models.PROTECT, verbose_name='Тип рациона')

    class Meta:
        verbose_name = 'Рацион'
        verbose_name_plural = 'Рационы'

    def __str__(self):
        return f"{self.number} - {self.name}"

# Зона обитания
class Habitat(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название зоны')
    continent = models.CharField(max_length=100, verbose_name='Материк')
    country = models.CharField(max_length=100, verbose_name='Страна')
    description = models.TextField(blank=True, verbose_name='Характеристика')

    class Meta:
        verbose_name = 'Зона обитания'
        verbose_name_plural = 'Зоны обитания'

    def __str__(self):
        return self.name

# Зоопарк (для аренды/собственности)
class Zoo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название зоопарка')
    address = models.TextField(verbose_name='Адрес')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    contact_email = models.EmailField(blank=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Зоопарк'
        verbose_name_plural = 'Зоопарки'

    def __str__(self):
        return self.name

# Место зимовки для птиц
class WinteringPlace(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    country = models.CharField(max_length=100, verbose_name='Страна')
    name = models.CharField(max_length=200, blank=True, verbose_name='Название места')

    class Meta:
        verbose_name = 'Место зимовки'
        verbose_name_plural = 'Места зимовки'

    def __str__(self):
        return f"{self.code} - {self.country}"

# Отдел зоопарка
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название отдела')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name

# Здание
class Building(models.Model):
    BUILDING_TYPE_CHOICES = [
        ('summer', 'Летнее'),
        ('winter', 'Зимнее'),
    ]
    name = models.CharField(max_length=100, verbose_name='Название здания')
    building_type = models.CharField(max_length=10, choices=BUILDING_TYPE_CHOICES, verbose_name='Тип здания')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='buildings', verbose_name='Отдел')

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'

    def __str__(self):
        return f"{self.name} ({self.get_building_type_display()})"

# Вольер
class Enclosure(models.Model):
    number = models.CharField(max_length=20, verbose_name='Номер вольера')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='enclosures', verbose_name='Отдел')
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True, related_name='enclosures', verbose_name='Здание')
    is_communal = models.BooleanField(default=False, verbose_name='Коммунальная квартира')
    has_pool = models.BooleanField(default=False, verbose_name='Наличие бассейна')
    has_equipment = models.BooleanField(default=False, verbose_name='Дополнительное оборудование')
    has_indoor = models.BooleanField(default=False, verbose_name='Внутреннее помещение')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')

    class Meta:
        verbose_name = 'Вольер'
        verbose_name_plural = 'Вольеры'
        unique_together = ('department', 'number')  # в пределах отдела номер уникален

    def __str__(self):
        return f"Вольер {self.number} ({self.department.name})"

# Сотрудник (общая информация)
class Staff(models.Model):
    STAFF_TYPE_CHOICES = [
        ('caretaker', 'Смотритель'),
        ('vet', 'Ветеринар'),
    ]
    personnel_number = models.CharField(max_length=20, unique=True, verbose_name='Табельный номер')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    staff_type = models.CharField(max_length=10, choices=STAFF_TYPE_CHOICES, verbose_name='Тип сотрудника')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.full_name} ({self.get_staff_type_display()})"

# Животное (основная модель)
class Animal(models.Model):
    GENDER_CHOICES = [
        ('M', 'Самец'),
        ('F', 'Самка'),
    ]
    ANIMAL_TYPE_CHOICES = [
        ('mammal', 'Млекопитающее'),
        ('bird', 'Птица'),
        ('reptile', 'Рептилия'),
    ]
    OWNERSHIP_CHOICES = [
        ('own', 'Собственность зоопарка'),
        ('lease', 'Аренда'),
    ]

    # Основные поля
    unique_number = models.CharField(max_length=50, unique=True, verbose_name='Уникальный номер')
    name = models.CharField(max_length=200, verbose_name='Имя')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    animal_type = models.CharField(max_length=10, choices=ANIMAL_TYPE_CHOICES, verbose_name='Тип животного')
    habitat = models.ForeignKey(Habitat, on_delete=models.PROTECT, related_name='animals', verbose_name='Зона обитания')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='animals', verbose_name='Отдел')
    current_enclosure = models.ForeignKey(Enclosure, on_delete=models.PROTECT, related_name='animals', verbose_name='Текущий вольер')

    # Поля для птиц
    wintering_place = models.ForeignKey(WinteringPlace, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Место зимовки')
    departure_date = models.DateField(null=True, blank=True, verbose_name='Дата улёта')
    return_date = models.DateField(null=True, blank=True, verbose_name='Дата прилёта')   # было arrival_date


    # Дополнительные поля для рептилий
    normal_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Нормальная температура')
    hibernation_start = models.DateField(null=True, blank=True, verbose_name='Начало спячки')
    hibernation_end = models.DateField(null=True, blank=True, verbose_name='Конец спячки')

    # Информация о собственности
    ownership_type = models.CharField(max_length=5, choices=OWNERSHIP_CHOICES, verbose_name='Тип собственности')
    owner_zoo = models.ForeignKey(Zoo, on_delete=models.SET_NULL, null=True, blank=True, related_name='leased_animals', verbose_name='Зоопарк-владелец (аренда)')
    lease_start = models.DateField(null=True, blank=True, verbose_name='Начало аренды')
    lease_end = models.DateField(null=True, blank=True, verbose_name='Окончание аренды')
    lease_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Стоимость аренды')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='Дата покупки')
    seller_organization = models.CharField(max_length=200, blank=True, verbose_name='Организация-продавец')
    arrival_date = models.DateField(verbose_name='Дата поступления в зоопарк')

    # Связи с сотрудниками (многие ко многим через промежуточные модели)
    caretakers = models.ManyToManyField(Staff, through='CaretakerAssignment', related_name='animals_cared', limit_choices_to={'staff_type': 'caretaker'})
    veterinarians = models.ManyToManyField(Staff, through='VeterinarianAssignment', related_name='animals_vetted', limit_choices_to={'staff_type': 'vet'})

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return f"{self.unique_number} - {self.name}"

# История назначения рационов
class FeedingHistory(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feeding_history')
    ration = models.ForeignKey(FeedingRation, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'История кормления'
        verbose_name_plural = 'Истории кормления'

# Назначение смотрителей
class CaretakerAssignment(models.Model):
    caretaker = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'staff_type': 'caretaker'})
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Назначение смотрителя'
        verbose_name_plural = 'Назначения смотрителей'

# Назначение ветеринаров
class VeterinarianAssignment(models.Model):
    veterinarian = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'staff_type': 'vet'})
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Назначение ветеринара'
        verbose_name_plural = 'Назначения ветеринаров'

# История пересадок
class TransferHistory(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='transfer_history')
    from_enclosure = models.ForeignKey(Enclosure, on_delete=models.PROTECT, related_name='transfers_from')
    to_enclosure = models.ForeignKey(Enclosure, on_delete=models.PROTECT, related_name='transfers_to')
    transfer_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'История пересадок'
        verbose_name_plural = 'Истории пересадок'




