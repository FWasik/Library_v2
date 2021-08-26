from rest_framework import viewsets, permissions
from .models import Author, Book, Order
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    OrderSerializer,
    )


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
