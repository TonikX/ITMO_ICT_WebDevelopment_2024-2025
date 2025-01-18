from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=500)
    winter_place = models.BooleanField
    area = models.ForeignKey('system.Area', related_name='buildings', on_delete=models.CASCADE,
                            null=True, blank=True)


class Cage(models.Model):
    name = models.CharField(max_length=500)
    building = models.ForeignKey('system.Building', related_name='cages', on_delete=models.CASCADE,
                            null=True, blank=True)
    
    communal = models.BooleanField()
    additional = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name


class Diet(models.Model):
    num = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Habitat(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    characteristic = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Animal(models.Model):
    num = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=500)
    age = models.IntegerField()
    sex = models.TextField(max_length=2, choices=(('m', 'm'), ('f', 'f')))
    birthdate = models.DateField()
    diet = models.ForeignKey('system.Diet', related_name='animals_on_this_diet', on_delete=models.CASCADE,
                             null=True, blank=True)

    winter_place = models.ForeignKey('system.WinterPlace', related_name='birds_wintering', on_delete=models.CASCADE,
                                     null=True, blank=True)

    habitat_place = models.ForeignKey('system.Habitat', related_name='animals', on_delete=models.CASCADE,
                                     null=True, blank=True)

    winter_sleeping = models.IntegerField(null=True, blank=True)
    normal_temperature = models.FloatField(null=True, blank=True)

    owner = models.CharField(max_length=2000)
    previous_owner = models.CharField(max_length=2000)

    in_lease = models.BooleanField()
    leaser_name = models.CharField(max_length=2000, null=True, blank=True)

    since = models.DateField()

    def __str__(self):
        return self.name


class WinterPlace(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=500)
    date_to = models.DateField()
    date_from = models.DateField()

    def __str__(self):
        return self.name


class AnimalInCage(models.Model):
    animal = models.OneToOneField('system.Animal', related_name='where', on_delete=models.CASCADE,
                                  null=True, blank=True)
    cage = models.ForeignKey('system.Cage', related_name='who', on_delete=models.CASCADE,
                               null=True, blank=True)

    def __str__(self):
        return f"{self.animal} in {self.cage}"


class Worker(models.Model):
    num = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=500)
    birthday = models.DateField()
    animals = models.ManyToManyField('system.Animal', related_name='wathers')
    passport = models.CharField(max_length=20, unique=True, blank=True,  null=True)
    email = models.CharField(max_length=100, unique=True, blank=True,  null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name



