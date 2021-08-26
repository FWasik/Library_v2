from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer, ProfileSerializer
from .models import CustomUser


#Permission for some methods
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]

        if self.request.method in ['DELETE', 'PATCH', 'PUT']:
            return [IsOwnerOrAdmin()]

        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]

    def retrieve(self, request, *args, **kwargs):
        is_owner = self.get_object()

        if is_owner == request.user or request.user.is_staff:
            return super(UserViewSet, self).retrieve(request)

        self.serializer_class = ProfileSerializer
        return super(UserViewSet, self).retrieve(request)

