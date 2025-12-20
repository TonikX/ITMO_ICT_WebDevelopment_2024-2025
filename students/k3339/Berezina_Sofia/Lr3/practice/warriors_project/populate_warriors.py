import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warriors_project.settings')
django.setup()

from warriors_app.models import Warrior, Profession, Skill, SkillOfWarrior
from django.db import transaction


def create_warriors():
    print("Начинаем заполнение базы данных воинами...")

    # Очистка старых данных (опционально)
    SkillOfWarrior.objects.all().delete()
    Warrior.objects.all().delete()
    Profession.objects.all().delete()
    Skill.objects.all().delete()

    # Создание профессий
    print("Создание профессий...")
    professions = [
        Profession(title="Воин", description="Сильный и выносливый боец ближнего боя"),
        Profession(title="Лучник", description="Меткий стрелок из лука"),
        Profession(title="Маг", description="Владеет магическими искусствами"),
        Profession(title="Лекарь", description="Исцеляет раны и болезни"),
        Profession(title="Разведчик", description="Мастер скрытности и разведки"),
    ]

    for profession in professions:
        profession.save()
        print(f"  Создана профессия: {profession.title}")

    # Создание умений
    print("\nСоздание умений...")
    skills = [
        Skill(title="Меч"),
        Skill(title="Лук"),
        Skill(title="Магия огня"),
        Skill(title="Магия льда"),
        Skill(title="Исцеление"),
        Skill(title="Скрытность"),
        Skill(title="Защита"),
        Skill(title="Критический удар"),
        Skill(title="Тактика"),
        Skill(title="Выживание"),
    ]

    for skill in skills:
        skill.save()
        print(f"  Создано умение: {skill.title}")

    # Создание воинов
    print("\nСоздание воинов...")
    warriors_data = [
        {
            "name": "Арагорн",
            "race": "s",
            "level": 45,
            "profession": professions[0],
            "skills": [
                {"skill": skills[0], "level": 8},  # Меч
                {"skill": skills[6], "level": 7},  # Защита
                {"skill": skills[8], "level": 9},  # Тактика
            ]
        },
        {
            "name": "Леголас",
            "race": "d",
            "level": 42,
            "profession": professions[1],
            "skills": [
                {"skill": skills[1], "level": 10},  # Лук
                {"skill": skills[7], "level": 8},  # Критический удар
                {"skill": skills[5], "level": 6},  # Скрытность
            ]
        },
        {
            "name": "Гэндальф",
            "race": "t",
            "level": 99,
            "profession": professions[2],
            "skills": [
                {"skill": skills[2], "level": 10},  # Магия огня
                {"skill": skills[3], "level": 9},  # Магия льда
                {"skill": skills[6], "level": 7},  # Защита
            ]
        },
        {
            "name": "Эовин",
            "race": "s",
            "level": 38,
            "profession": professions[0],
            "skills": [
                {"skill": skills[0], "level": 7},  # Меч
                {"skill": skills[4], "level": 6},  # Исцеление
                {"skill": skills[8], "level": 5},  # Тактика
            ]
        },
        {
            "name": "Фродо",
            "race": "d",
            "level": 25,
            "profession": professions[4],
            "skills": [
                {"skill": skills[5], "level": 8},  # Скрытность
                {"skill": skills[9], "level": 7},  # Выживание
                {"skill": skills[7], "level": 4},  # Критический удар
            ]
        },
        {
            "name": "Саруман",
            "race": "t",
            "level": 85,
            "profession": professions[2],
            "skills": [
                {"skill": skills[2], "level": 9},  # Магия огня
                {"skill": skills[3], "level": 8},  # Магия льда
                {"skill": skills[8], "level": 7},  # Тактика
            ]
        },
        {
            "name": "Гимли",
            "race": "s",
            "level": 48,
            "profession": professions[0],
            "skills": [
                {"skill": skills[0], "level": 9},  # Меч
                {"skill": skills[6], "level": 8},  # Защита
                {"skill": skills[9], "level": 6},  # Выживание
            ]
        },
        {
            "name": "Арвен",
            "race": "d",
            "level": 65,
            "profession": professions[3],
            "skills": [
                {"skill": skills[4], "level": 10},  # Исцеление
                {"skill": skills[1], "level": 7},  # Лук
                {"skill": skills[3], "level": 6},  # Магия льда
            ]
        },
    ]

    with transaction.atomic():
        for warrior_data in warriors_data:
            warrior = Warrior(
                name=warrior_data["name"],
                race=warrior_data["race"],
                level=warrior_data["level"],
                profession=warrior_data["profession"]
            )
            warrior.save()

            # Добавляем умения через промежуточную модель
            for skill_data in warrior_data["skills"]:
                SkillOfWarrior.objects.create(
                    warrior=warrior,
                    skill=skill_data["skill"],
                    level=skill_data["level"]
                )

            print(f"  Создан воин: {warrior.name} (уровень {warrior.level})")

    # Вывод статистики
    print("\n" + "=" * 50)
    print("СТАТИСТИКА БАЗЫ ДАННЫХ:")
    print(f"Всего воинов: {Warrior.objects.count()}")
    print(f"Всего профессий: {Profession.objects.count()}")
    print(f"Всего умений: {Skill.objects.count()}")
    print(f"Всего связей воин-умение: {SkillOfWarrior.objects.count()}")

    print("\nРаспределение по расам:")
    from django.db.models import Count
    race_stats = Warrior.objects.values('race').annotate(total=Count('id'))
    for stat in race_stats:
        race_name = dict(Warrior.race_types)[stat['race']]
        print(f"  {race_name}: {stat['total']} воинов")

    print("\nВоин с самым высоким уровнем:")
    strongest = Warrior.objects.order_by('-level').first()
    print(f"  {strongest.name} - уровень {strongest.level}")

    print("\nСамое популярное умение:")
    from django.db.models import Count
    popular_skill = Skill.objects.annotate(warrior_count=Count('skillofwarrior')).order_by('-warrior_count').first()
    print(f"  {popular_skill.title} - {popular_skill.warrior_count} воинов")


if __name__ == "__main__":
    create_warriors()