import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_drf_project.settings')
django.setup()

import random
from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior

RACE_TYPES = ['s', 'd', 't']

NAMES = ['Arthas', 'Jaina', 'Thrall', 'Sylvanas', 'Varian', 'Illidan', 'Guldan']

PROFESSIONS = [
    {"title": "Warrior", "description": "A brave and skilled fighter."},
    {"title": "Mage", "description": "A master of arcane arts and spells."},
    {"title": "Rogue", "description": "An agile and stealthy assassin."},
    {"title": "Priest", "description": "A healer and protector of the weak."},
    {"title": "Hunter", "description": "An expert tracker and sharpshooter."},
]

SKILLS = ['Swordsmanship', 'Archery', 'Magic', 'Stealth', 'Alchemy', 'Cooking', 'Healing']


def generate_professions():
    for profession in PROFESSIONS:
        Profession.objects.create(title=profession['title'], description=profession['description'])
    print(f"{len(PROFESSIONS)} профессий создано.")


def generate_skills():
    for skill in SKILLS:
        Skill.objects.create(title=skill)
    print(f"{len(SKILLS)} умений создано.")


def generate_warriors(num=10):
    professions = list(Profession.objects.all())
    skills = list(Skill.objects.all())

    for _ in range(num):
        name = random.choice(NAMES)
        race = random.choice(RACE_TYPES)
        level = random.randint(1, 100)
        profession = random.choice(professions) if professions else None

        warrior = Warrior.objects.create(name=name, race=race, level=level, profession=profession)

        for _ in range(random.randint(1, 3)):
            skill = random.choice(skills)
            skill_level = random.randint(1, 10)
            SkillOfWarrior.objects.create(warrior=warrior, skill=skill, level=skill_level)

    print(f"{num} воинов создано.")


def run():
    print("Начинаем генерацию данных...")
    generate_professions()
    generate_skills()
    generate_warriors(10)
    print("Генерация данных завершена.")


if __name__ == "__main__":
    run()
