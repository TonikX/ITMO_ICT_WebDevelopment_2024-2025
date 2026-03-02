from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated

from .models import Category, Task, Tag
from .serializers import (
    CategorySerializer,
    TaskSerializer,
    TaskNestedSerializer,
    CategoryNestedSerializer,
    TagSerializer,
)

# ---------- TAG ----------

class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # если у тебя теги привязаны к owner, оставь так:
        return Tag.objects.filter(owner=self.request.user)

        # если owner не нужен и теги общие, замени на:
        # return Tag.objects.all()

    def perform_create(self, serializer):
        if not self.request.user or not self.request.user.is_authenticated:
            raise NotAuthenticated("Token not provided or invalid")
        serializer.save(owner=self.request.user)


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


# ---------- CATEGORY ----------

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class CategoryWithTasksView(generics.ListAPIView):
    serializer_class = CategoryNestedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


# ---------- TASK ----------

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskFullInfoView(generics.ListAPIView):
    serializer_class = TaskNestedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
