from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer

class MyProfileView(generics.RetrieveUpdateAPIView):
    """Получить/обновить профиль текущего пользователя.

    Роль менять нельзя
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserProfileUpdateSerializer
        return UserProfileSerializer
