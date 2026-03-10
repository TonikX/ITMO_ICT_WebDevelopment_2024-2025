from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserRole

def get_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return UserRole.ADMIN
    try:
        return user.profile.role
    except Exception:
        return None

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == UserRole.ADMIN

class IsCaptain(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == UserRole.CAPTAIN

class IsCurator(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == UserRole.CURATOR

class IsJury(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == UserRole.JURY

class TaskWritePermission(BasePermission):
    """Создавать/редактировать задачи может только главный админ."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return get_role(request.user) == UserRole.ADMIN

class TeamPermission(BasePermission):
    """Команду может создавать/редактировать только капитан этой команды.
    Просматривать команды: админ, куратор, жюри (для сортировок/аналитики) и капитан своей команды.
    """
    def has_permission(self, request, view):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # create/update/delete
        return role == UserRole.CAPTAIN

    def has_object_permission(self, request, view, obj):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            if role in (UserRole.ADMIN, UserRole.CURATOR, UserRole.JURY):
                return True
            return obj.captain_id == request.user.id
        return obj.captain_id == request.user.id

class TaskResourcePermission(BasePermission):
    """Редактировать ресурсы задачи может только куратор своей задачи или админ."""
    def has_permission(self, request, view):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return role in (UserRole.ADMIN, UserRole.CURATOR)

    def has_object_permission(self, request, view, obj):
        role = get_role(request.user)
        if role == UserRole.ADMIN:
            return True
        if role == UserRole.CURATOR:
            # куратор может править только свою задачу
            return obj.task.curator_id == request.user.id
        return request.method in SAFE_METHODS

class SolutionPermission(BasePermission):
    """Решения:
    - капитан может создавать/редактировать решения своей команды
    - куратор видит решения по своей задаче
    - жюри видит все решения
    - админ видит все решения
    """
    def has_permission(self, request, view):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return role == UserRole.CAPTAIN or role == UserRole.ADMIN

    def has_object_permission(self, request, view, obj):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            if role == UserRole.ADMIN:
                return True
            if role == UserRole.JURY:
                return True
            if role == UserRole.CURATOR:
                return obj.task.curator_id == request.user.id
            if role == UserRole.CAPTAIN:
                return obj.team.captain_id == request.user.id
            return False

        # write
        if role == UserRole.ADMIN:
            return True
        return obj.team.captain_id == request.user.id

class EvaluationPermission(BasePermission):
    """Оценки может создавать жюри, редактировать только автор оценки.
    Смотреть могут жюри/куратор(по своей задаче)/админ/капитан (по своей команде).
    """
    def has_permission(self, request, view):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return role == UserRole.JURY

    def has_object_permission(self, request, view, obj):
        role = get_role(request.user)
        if request.method in SAFE_METHODS:
            if role == UserRole.ADMIN:
                return True
            if role == UserRole.JURY:
                return True
            if role == UserRole.CURATOR:
                return obj.solution.task.curator_id == request.user.id
            if role == UserRole.CAPTAIN:
                return obj.solution.team.captain_id == request.user.id
            return False
        # write: только автор
        return obj.jury_member_id == request.user.id
