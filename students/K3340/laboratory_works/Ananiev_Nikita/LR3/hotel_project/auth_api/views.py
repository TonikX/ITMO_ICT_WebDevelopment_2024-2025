from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
# from yaml import serialize

from .serializers import *

class UserAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = UserAccount.objects.all()


class UserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = UserAccount.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'id'
    queryset = UserAccount.objects.all()
