from django.http import HttpResponseForbidden

def participant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'participant'):
            return HttpResponseForbidden("Доступ разрешён только зарегистрированным гонщикам.")
        return view_func(request, *args, **kwargs)
    return wrapper
