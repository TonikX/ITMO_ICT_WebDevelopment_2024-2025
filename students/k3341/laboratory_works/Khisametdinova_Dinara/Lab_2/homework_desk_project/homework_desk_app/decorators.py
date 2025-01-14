from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def is_admin_or_teacher(user):
    return user.is_superuser or user.role == 'teacher'

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect('student_homework_list') 
    return login_required(wrapper)

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('homeworks') 
    return login_required(wrapper)