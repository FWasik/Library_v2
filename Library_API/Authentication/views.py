from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = CustomUserSerializer

