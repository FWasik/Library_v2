from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer#, ProfileSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


#Permission for some methods
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'

    parser_classes = (MultiPartParser, FormParser,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]

        if self.request.method in ['DELETE', 'PATCH', 'PUT', 'GET']:
            return [IsOwnerOrAdmin()]

        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(UserViewSet, self).list(request)

        content = {
            'Unauthorized': 'Brak autoryzacji!'
        }

        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.image.name == 'default.jpg':
            user.image.delete()

        return super(UserViewSet, self).destroy(request)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
