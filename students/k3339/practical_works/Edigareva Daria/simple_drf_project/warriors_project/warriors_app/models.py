from django.db import models


class Warrior(models.Model):
    race_types = (
        ('s', 'student'),
        ('d', 'developer'),
        ('t', 'teamlead'),
    )
    race = models.CharField(max_length=1, choices=race_types, verbose_name='Расса')
    name = models.CharField(max_length=120, verbose_name='Имя')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    skill = models.ManyToManyField('Skill', through='SkillOfWarrior', related_name='warrior_skils')
    profession = models.ForeignKey('Profession', on_delete=models.CASCADE, blank=True, null=True)


class Profession(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()


class Skill(models.Model):
    title = models.CharField(max_length=120)


class SkillOfWarrior(models.Model):
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    warrior = models.ForeignKey('Warrior', on_delete=models.CASCADE)
    level = models.IntegerField()
