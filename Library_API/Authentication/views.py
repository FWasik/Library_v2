from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer
from .models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    serializer_class = CustomUserSerializer

