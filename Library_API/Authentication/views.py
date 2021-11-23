from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer#, ProfileSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response


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

        content = {
            'Unauthorized': 'You are not authorized for that action'
        }

        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(UserViewSet, self).list(request)

        content = {
            'Unauthorized': 'You are not authorized for that action'
        }

        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

