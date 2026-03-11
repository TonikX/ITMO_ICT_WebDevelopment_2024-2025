from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers import UserShortSerializer
from .models import (
    Tag, Task, TaskResourceLink, TaskResourceFile,
    Team, TeamMember, Solution, SolutionAttachment, Evaluation,
    SolutionStatus
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

class TaskResourceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResourceLink
        fields = ("id", "title", "url")

class TaskResourceFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = TaskResourceFile
        fields = ("id", "title", "file", "file_url")
        extra_kwargs = {"file": {"write_only": True}}

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not obj.file:
            return ""
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class TaskSerializer(serializers.ModelSerializer):
    """Вложенная сериализация: связи 1-to-many и many-to-many."""
    curator = UserShortSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    resource_links = TaskResourceLinkSerializer(many=True, read_only=True)
    resource_files = TaskResourceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id", "title", "description", "curator", "consultation_url",
            "tags", "resource_links", "resource_files", "created_at"
        )

class TaskWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/редактирования задачи админом."""
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "description", "curator", "consultation_url", "tag_ids")

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        task = super().create(validated_data)
        if tag_ids:
            task.tags.set(Tag.objects.filter(id__in=tag_ids))
        return task

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)
        task = super().update(instance, validated_data)
        if tag_ids is not None:
            task.tags.set(Tag.objects.filter(id__in=tag_ids))
        return task

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ("id", "full_name", "email", "role_in_team")

class TeamSerializer(serializers.ModelSerializer):
    captain = UserShortSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    selected_task = TaskSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "captain", "name", "motto", "selected_task", "members", "created_at")

class TeamWriteSerializer(serializers.ModelSerializer):
    """Создание/обновление команды капитаном."""
    member_items = TeamMemberSerializer(many=True, required=False, write_only=True)
    selected_task_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Team
        fields = ("id", "name", "motto", "selected_task_id", "member_items")

    def validate(self, attrs):
        # капитан не должен создавать несколько команд (OneToOne гарантирует, но выдадим понятную ошибку)
        user = self.context["request"].user
        if self.instance is None and hasattr(user, "team"):
            raise serializers.ValidationError("У этого капитана уже есть команда.")
        return attrs

    def create(self, validated_data):
        members = validated_data.pop("member_items", [])
        selected_task_id = validated_data.pop("selected_task_id", None)
        user = self.context["request"].user

        team = Team.objects.create(captain=user, **validated_data)

        if selected_task_id:
            team.selected_task_id = selected_task_id
            team.save()

        # создаём участников команды
        for m in members:
            TeamMember.objects.create(team=team, **m)
        return team

    def update(self, instance, validated_data):
        members = validated_data.pop("member_items", None)
        selected_task_id = validated_data.pop("selected_task_id", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)

        if selected_task_id is not None:
            instance.selected_task_id = selected_task_id

        instance.save()

        # если передали member_items — перезаписываем состав (просто, но логично для ЛР)
        if members is not None:
            instance.members.all().delete()
            for m in members:
                TeamMember.objects.create(team=instance, **m)

        return instance

class SolutionAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = SolutionAttachment
        fields = ("id", "title", "file", "file_url")
        extra_kwargs = {"file": {"write_only": True}}

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not obj.file:
            return ""
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url

class SolutionSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    attachments = SolutionAttachmentSerializer(many=True, read_only=True)

    avg_score = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = (
            "id", "team", "task", "title", "description", "repo_url",
            "status", "created_at", "submitted_at", "attachments", "avg_score"
        )

    def get_avg_score(self, obj):
        # средняя оценка по оценкам жюри (для демонстрации аналитики на уровне объекта)
        qs = obj.evaluations.all()
        if not qs.exists():
            return None
        return round(sum(e.score for e in qs) / qs.count(), 2)

class SolutionWriteSerializer(serializers.ModelSerializer):
    """Создание/обновление решения капитаном."""
    task_id = serializers.IntegerField(write_only=True)
    attachment_items = SolutionAttachmentSerializer(many=True, required=False, write_only=True)
    submit = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Solution
        fields = ("id", "task_id", "title", "description", "repo_url", "status", "attachment_items", "submit")

    def validate_task_id(self, value):
        from .models import Task
        if not Task.objects.filter(id=value).exists():
            raise serializers.ValidationError("Задача не найдена.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        if not hasattr(user, "team"):
            raise serializers.ValidationError("Сначала создайте команду.")
        team = user.team
        task_id = attrs.get("task_id")

        # Команда должна выбрать задачу и отправлять решение только по выбранной задаче
        if team.selected_task_id is None:
            raise serializers.ValidationError("Сначала выберите задачу для команды (selected_task).")
        if task_id is not None and team.selected_task_id != task_id:
            raise serializers.ValidationError("Нельзя отправить решение по задаче, отличной от выбранной.")
        return attrs

    def create(self, validated_data):
        from django.utils import timezone
        user = self.context["request"].user
        team = user.team
        attachment_items = validated_data.pop("attachment_items", [])
        submit = validated_data.pop("submit", False)
        task_id = validated_data.pop("task_id")

        sol = Solution.objects.create(team=team, task_id=task_id, **validated_data)

        for a in attachment_items:
            SolutionAttachment.objects.create(solution=sol, **a)

        if submit:
            sol.status = SolutionStatus.SUBMITTED
            sol.submitted_at = timezone.now()
            sol.save()

        return sol

    def update(self, instance, validated_data):
        from django.utils import timezone
        attachment_items = validated_data.pop("attachment_items", None)
        submit = validated_data.pop("submit", None)
        validated_data.pop("task_id", None)  # задачу менять нельзя

        # нельзя редактировать отправленное решение (правило можно менять, но так логично)
        if instance.status == SolutionStatus.SUBMITTED:
            raise serializers.ValidationError("Нельзя редактировать уже отправленное решение.")

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if attachment_items is not None:
            instance.attachments.all().delete()
            for a in attachment_items:
                SolutionAttachment.objects.create(solution=instance, **a)

        if submit:
            instance.status = SolutionStatus.SUBMITTED
            instance.submitted_at = timezone.now()
            instance.save()

        return instance

class EvaluationSerializer(serializers.ModelSerializer):
    jury_member = UserShortSerializer(read_only=True)

    class Meta:
        model = Evaluation
        fields = ("id", "solution", "jury_member", "score", "comment", "created_at")
        read_only_fields = ("jury_member",)

class EvaluationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ("id", "solution", "score", "comment")

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("score должен быть в диапазоне 0..10.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return Evaluation.objects.create(jury_member=user, **validated_data)
