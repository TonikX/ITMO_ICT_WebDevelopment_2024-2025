from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    """Тег/технология для задачи.
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    """Задача хакатона.

    Главный администратор создаёт задачу, затем назначает на неё куратора.
    Куратор может быть назначен только на одну задачу (ограничение реализовано через OneToOne).
    """
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Куратор ведёт одну задачу, поэтому OneToOne + related_name для удобных запросов.
    curator = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="curated_task"
    )

    # M2M теги
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    # Ссылка на консультацию
    consultation_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskResourceLink(models.Model):
    """Ссылка, прикреплённая к задаче (например, документация/репозиторий/формы)."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="resource_links")
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return f"{self.task_id}: {self.title}"

class TaskResourceFile(models.Model):
    """Файл, прикреплённый к задаче (например, исходники/датасеты/шаблоны)."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="resource_files")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="task_files/")

    def __str__(self):
        return f"{self.task_id}: {self.title}"

class Team(models.Model):
    """Команда.

    В системе регистрируется только капитан (User). Участники команды — отдельные записи TeamMember.
    """
    captain = models.OneToOneField(User, on_delete=models.CASCADE, related_name="team")
    name = models.CharField(max_length=255)
    motto = models.CharField(max_length=255, blank=True)

    # Команда выбирает одну задачу (по ТЗ: выбрать одну из задач)
    selected_task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    """Участник команды (не является пользователем системы)."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    role_in_team = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.team_id}: {self.full_name}"

class SolutionStatus(models.TextChoices):
    DRAFT = "DRAFT", "Черновик"
    SUBMITTED = "SUBMITTED", "Отправлено"

class Solution(models.Model):
    """Решение команды.

    Команда (капитан) после выбора задачи может отправить решение.
    Жюри и куратор имеют доступ к решениям (с ограничениями по роли).
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="solutions")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="solutions")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=SolutionStatus.choices, default=SolutionStatus.DRAFT)

    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.team.name}: {self.title}"

class SolutionAttachment(models.Model):
    """Файл-аттачмент к решению."""
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="attachments")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="solution_files/")

class Evaluation(models.Model):
    """Оценка решения членом жюри."""
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="evaluations")
    jury_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evaluations_given")

    score = models.PositiveSmallIntegerField()  # например 0..10, проверим в сериализаторе
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("solution", "jury_member")  # один член жюри оценивает решение один раз

    def __str__(self):
        return f"{self.solution_id} by {self.jury_member.username}: {self.score}"
