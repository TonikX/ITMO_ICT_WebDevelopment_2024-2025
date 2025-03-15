from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Pet(models.Model):

    number = models.IntegerField(primary_key=True)
    
    sex_types = (
        ("f", "самка"),
        ("m", "самец")
    )
    sex = models.CharField(choices=sex_types, max_length=1)
    name = models.CharField(max_length=100)
    birtday = models.DateField()

    animal_type = models.CharField(max_length=100)
    is_buy = models.BooleanField()
    rented_types = (
        ("in", "Взят"),
        ("out", "Сдан")
    )
    is_rented = models.CharField(max_length=3, choices=rented_types, null=True, blank=True)

    valliere = models.ForeignKey("Valliere", on_delete=models.PROTECT, related_name="pets")
    habited = models.ForeignKey("Habited", on_delete=models.SET_NULL, null=True, blank=True, related_name="pets")
    diet = models.ForeignKey("Diet", on_delete=models.PROTECT, related_name="pets")


class NoteReptile(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="note_reptile_pet")
    normal_temperature = models.IntegerField()
    begin_wintering = models.DateField()


class NoteBird(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="note_bird_pet")
    is_wintering = models.BooleanField()
    country_wintering = models.CharField(max_length=100, null=True, blank=True)
    start_wintering = models.DateField(null=True, blank=True)
    finish_wintering = models.DateField(null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.is_wintering:
            if None in [self.country_wintering, self.start_wintering, self.finish_wintering]:
                raise ValidationError('Для зимующих птиц все параметры обязательны')
        else:
            if not any([self.country_wintering, self.start_wintering, self.finish_wintering]):
                raise ValidationError('Для незимующих птиц все параметры должны быть пусты')
            
        if self.finish_wintering < self.start_wintering:
            raise ValidationError('Дата окончания не может быть меньше даты начала')


class Buy(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="buy_pet")
    seller = models.CharField(max_length=100)
    date_buy = models.DateField()


class Rent(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name="rent_pet")
    zoo = models.CharField(max_length=100)
    price = models.IntegerField()
    start_rent = models.DateField()
    finish_rent = models.DateField()

    def clean(self) -> None:
        super().clean()

        if self.finish_rent < self.start_rent:
            raise ValidationError('Дата окончания не может быть меньше даты начала')


class Valliere(models.Model):
    is_commun = models.BooleanField()
    is_isolated = models.BooleanField()
    building = models.ForeignKey("Building", on_delete=models.CASCADE)
    params = models.ManyToManyField("Valliere_Parameter", blank=True)


class Valliere_Parameter(models.Model):
    title = models.CharField(max_length=100)


class Building(models.Model):
    build_types = (
        ("s", "летнее"),
        ("w", "зимнее")
    )
    type_build = models.CharField(max_length=1, choices=build_types)
    depart = models.CharField(max_length=100)


class Habited(models.Model):
    name = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()


class Diet(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type_diet = models.CharField(max_length=40)
    products = models.ManyToManyField("Product")


class Product(models.Model):
    name = models.CharField(max_length=100)


class Employer(models.Model):
    employer_types = (
        ("v", "ветеринар"),
        ("z", "смотритель зоопарка"),
    )
    type_employer = models.CharField(max_length=1, choices=employer_types)
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    father_name = models.CharField(max_length=40, null=True, blank=True)
    birtday = models.DateField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(
        max_length = 20,
        validators = [
        RegexValidator(
            regex=r'^\+?\d{0,15}$',
            message="Введите корректный номер телефона."
          )
        ]
    )

    animals = models.ManyToManyField(Pet, related_name="employers_pet")