from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="Пользователь не найден.")

class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(detail="Пользователь не найден.")