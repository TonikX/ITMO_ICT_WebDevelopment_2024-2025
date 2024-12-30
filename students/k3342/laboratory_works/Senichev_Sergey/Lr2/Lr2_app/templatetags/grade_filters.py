from django import template

register = template.Library()


@register.filter
def get_grade(grades_dict, student_id):
    return grades_dict.get(student_id, {})


@register.filter
def get_task_grade(student_grades, task_id):
    return student_grades.get(task_id)
