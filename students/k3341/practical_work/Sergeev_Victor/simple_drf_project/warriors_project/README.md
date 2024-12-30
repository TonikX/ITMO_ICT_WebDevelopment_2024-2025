# Simple DRF project

## Usage

``python manage.py runserver``

## Project Models

### Warrior

- race - раса война (s - студент, d - разработчик, t - тимлидер)
- name - имя война (CharField, макс.длина=120)
- level - уровень война (IntegerField)
- skill - способности война (ManyToManyField с таблицей Skill, через таблица SkillOfWarrior)
- profession - профессия война (ForeignKey на таблицу Profession)

### Profession

- title - название профессии (CharField, макс.длина=120)
- description - описание профессии (TextField)

### Skill

- title - название способности(CharField, макс.длина=120)

### SkillOfWarrior

- skill - способность (ForeignKey на таблицу Skill)
- warrior - воин (ForeignKey на таблицу Warrior)
- level - уровень способности(IntegerField)

## Views

- ProfessionAPICreate - создание профессии
- SkillAPICreate - создание способности
- SkillAPIView - просмотр способности по id
- WarriorListAPIView - список войнов
- WarriorAPIView - просмотр, изменение и удаление война по id

## Documentation

Available on /doc/swagger
