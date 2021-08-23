from rest_framework import viewsets, permissions
from .models import Author, Book, Order
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    OrderSerializer,
    )


from rest_framework.authentication import TokenAuthentication


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny,]
    queryset = Author.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Book.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
