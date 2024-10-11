import enum
from datetime import UTC, datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Conference(models.Model):
    class Topic(enum.StrEnum):
        MATH = "Математика"
        PHYSIC = "Физика"
        IT = "Информационные технологии"

    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Название конференции",
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание конференции",
    )

    participation_conditions = models.TextField(
        null=True,
        blank=True,
        verbose_name="Условия участия в конференции",
    )

    is_publish = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Рекомендован к публикации или нет",
    )

    author = models.ForeignKey(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Автор конференции",
    )

    members = models.ManyToManyField(
        get_user_model(),
        related_name="conferences",
        verbose_name="Участники конференции",
        blank=True,
    )

    topics = ArrayField(
        models.CharField(
            max_length=15,
            choices=[(topic.name, topic.value) for topic in Topic],
        ),
        null=False,
        default=list,
        blank=False,
        verbose_name="Тематики",
    )

    class Meta:
        verbose_name = "Конференция"
        verbose_name_plural = "Конференции"
        db_table = "conference"

    def __str__(self) -> str:
        return f"Конференция: {self.name}"

    def count_members(self) -> int:
        return self.members.count()

    def is_started(self) -> bool:
        return self.booking.start_date <= datetime.now(UTC)

    def is_over(self) -> bool:
        return self.booking.end_date <= datetime.now(UTC)

    def display_topics(self) -> str:
        return ", ".join(map(lambda name: self.Topic[name], self.topics))

    def get_last_feedbacks(self):
        return self.feedbacks.order_by("-created_at")[:10]


class Feedback(models.Model):
    text = models.TextField(
        null=False,
        verbose_name="Текст комментария",
    )

    rating = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name="Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    author = models.ForeignKey(
        get_user_model(),
        null=False,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Автор комментария",
    )

    conference = models.ForeignKey(
        Conference,
        null=False,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        blank=False,
        verbose_name="Котференция",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False,
        verbose_name="Дата создания комментария",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        db_table = "feedback"

    def __str__(self) -> str:
        return f"Комментарий от пользователя {self.author.first_name} о конференции {self.conference.name}"


class Room(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Название коференц зала",
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание конференц зала",
    )

    seats = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name="Количество мест",
    )

    class Meta:
        verbose_name = "Конференц зал"
        verbose_name_plural = "Конференц залы"
        db_table = "room"

    def __str__(self) -> str:
        return self.name


class Booking(models.Model):
    start_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name="Дата начала бронирования",
    )

    end_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name="Дата окончания бронирования",
    )

    room = models.ForeignKey(
        Room,
        null=False,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Конференц зал",
    )

    conference = models.OneToOneField(
        Conference,
        null=True,
        on_delete=models.SET_NULL,
        related_name="booking",
        blank=True,
        verbose_name="Конференция",
    )

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Доступная бронь"
        db_table = "booking"

    def __str__(self) -> str:
        return "{} {}-{} {}".format(
            self.start_date.date().isoformat(),
            self.start_date.time().strftime("%H:%M"),
            self.end_date.time().strftime("%H:%M"),
            self.room,
        )
