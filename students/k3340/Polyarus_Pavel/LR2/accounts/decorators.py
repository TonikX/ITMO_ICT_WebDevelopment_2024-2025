from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def teacher_required(function=None):
    '''Декоратор для проверки что пользователь - преподаватель'''
    def check_teacher(user):
        if not user.is_authenticated:
            return False
        return hasattr(user, 'profile') and user.profile.is_teacher
    
    actual_decorator = user_passes_test(check_teacher)
    if function:
        return actual_decorator(function)
    return actual_decorator


def student_required(function=None):
    '''Декоратор для проверки что пользователь - студент'''
    def check_student(user):
        if not user.is_authenticated:
            return False
        return hasattr(user, 'profile') and user.profile.is_student
    
    actual_decorator = user_passes_test(check_student)
    if function:
        return actual_decorator(function)
    return actual_decorator