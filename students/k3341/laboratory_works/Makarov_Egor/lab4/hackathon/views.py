from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from django.contrib.auth.models import User

from .models import (
    Tag, Task, TaskResourceLink, TaskResourceFile,
    Team, Solution, Evaluation
)
from .serializers import (
    TagSerializer,
    TaskSerializer, TaskWriteSerializer,
    TaskResourceLinkSerializer, TaskResourceFileSerializer,
    TeamSerializer, TeamWriteSerializer,
    SolutionSerializer, SolutionWriteSerializer,
    EvaluationSerializer, EvaluationWriteSerializer,
)
from .permissions import (
    TaskWritePermission, TaskResourcePermission, TeamPermission,
    SolutionPermission, EvaluationPermission, get_role
)
from accounts.models import UserRole

class TagViewSet(viewsets.ModelViewSet):
    """CRUD тегов. Обычно управляет админ, но чтение доступно всем."""
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer
    permission_classes = [TaskWritePermission]

class TaskViewSet(viewsets.ModelViewSet):
    """CRUD задач.

    - Админ создаёт/редактирует задачи
    - Все авторизованные могут смотреть список/детали
    """
    queryset = Task.objects.all().prefetch_related("tags", "resource_links", "resource_files").select_related("curator").order_by("-created_at")
    permission_classes = [TaskWritePermission]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return TaskWriteSerializer
        return TaskSerializer

class TaskResourceLinkViewSet(viewsets.ModelViewSet):
    """CRUD ссылок ресурсов задачи.

    Изменять может куратор своей задачи или админ.
    """
    queryset = TaskResourceLink.objects.all().select_related("task")
    serializer_class = TaskResourceLinkSerializer
    permission_classes = [TaskResourcePermission]

    def perform_create(self, serializer):
        serializer.save()

class TaskResourceFileViewSet(viewsets.ModelViewSet):
    """CRUD файлов ресурсов задачи."""
    queryset = TaskResourceFile.objects.all().select_related("task")
    serializer_class = TaskResourceFileSerializer
    permission_classes = [TaskResourcePermission]

class TeamViewSet(viewsets.ModelViewSet):
    """CRUD команд.

    Капитан создаёт свою команду (одну) и редактирует её.
    """
    queryset = Team.objects.all().select_related("captain", "selected_task").prefetch_related("members").order_by("-created_at")
    permission_classes = [TeamPermission]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return TeamWriteSerializer
        return TeamSerializer

    def get_queryset(self):
        """Фильтруем выдачу по роли, чтобы соблюсти бизнес-логику."""
        user = self.request.user
        role = get_role(user)
        qs = super().get_queryset()

        if role in (UserRole.ADMIN, UserRole.JURY):
            return qs
        if role == UserRole.CURATOR:
            # куратор видит команды, выбравшие его задачу
            try:
                task = user.curated_task
                return qs.filter(selected_task=task)
            except Exception:
                return qs.none()
        if role == UserRole.CAPTAIN:
            return qs.filter(captain=user)
        return qs.none()

class SolutionViewSet(viewsets.ModelViewSet):
    """CRUD решений."""
    queryset = Solution.objects.all().select_related("team", "task", "team__captain", "task__curator").prefetch_related("attachments", "evaluations").order_by("-created_at")
    permission_classes = [SolutionPermission]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return SolutionWriteSerializer
        return SolutionSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)
        qs = super().get_queryset()

        if role == UserRole.ADMIN:
            return qs
        if role == UserRole.JURY:
            return qs
        if role == UserRole.CURATOR:
            # куратор видит решения только по своей задаче
            try:
                task = user.curated_task
                return qs.filter(task=task)
            except Exception:
                return qs.none()
        if role == UserRole.CAPTAIN:
            if hasattr(user, "team"):
                return qs.filter(team=user.team)
            return qs.none()
        return qs.none()

class EvaluationViewSet(viewsets.ModelViewSet):
    """CRUD оценок жюри."""
    queryset = Evaluation.objects.all().select_related("solution", "jury_member", "solution__task", "solution__team")
    permission_classes = [EvaluationPermission]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return EvaluationWriteSerializer
        return EvaluationSerializer

    def get_queryset(self):
        user = self.request.user
        role = get_role(user)
        qs = super().get_queryset().order_by("-created_at")

        if role == UserRole.ADMIN:
            return qs
        if role == UserRole.JURY:
            return qs  # жюри видит все оценки, но редактировать сможет только свои (object permission)
        if role == UserRole.CURATOR:
            try:
                task = user.curated_task
                return qs.filter(solution__task=task)
            except Exception:
                return qs.none()
        if role == UserRole.CAPTAIN:
            if hasattr(user, "team"):
                return qs.filter(solution__team=user.team)
            return qs.none()
        return qs.none()

    def perform_create(self, serializer):
        serializer.save()

class AnalyticsViewSet(viewsets.ViewSet):
    """Набор аналитических (агрегационных) запросов.

    Требование ЛР: придумать 3-4 агрегационных запроса.
    Здесь 4 запроса с использованием annotate/Count/Avg и связей (related_name).
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def teams_per_task(self, request):
        """Сколько команд выбрали каждую задачу."""
        data = Task.objects.annotate(teams_count=Count("teams")).values("id", "title", "teams_count").order_by("-teams_count", "title")
        return Response(list(data))

    @action(detail=False, methods=["get"])
    def avg_score_per_solution(self, request):
        """Средняя оценка по каждому решению (если оценок нет — будет null)."""
        data = Solution.objects.annotate(avg_score=Avg("evaluations__score")).values(
            "id", "title", "team__name", "task__title", "avg_score"
        ).order_by("-avg_score", "title")
        return Response(list(data))

    @action(detail=False, methods=["get"])
    def jury_activity(self, request):
        """Активность жюри: сколько оценок поставил каждый пользователь + средний балл, который он ставит."""
        data = User.objects.filter(profile__role=UserRole.JURY).annotate(
            eval_count=Count("evaluations_given"),
            avg_given=Avg("evaluations_given__score"),
        ).values("id", "username", "eval_count", "avg_given").order_by("-eval_count", "username")
        return Response(list(data))

    @action(detail=False, methods=["get"])
    def curator_load(self, request):
        """Нагрузка кураторов: сколько решений отправлено по задаче куратора."""
        data = User.objects.filter(profile__role=UserRole.CURATOR).annotate(
            submitted_solutions=Count("curated_task__solutions"),
        ).values("id", "username", "submitted_solutions").order_by("-submitted_solutions", "username")
        return Response(list(data))
