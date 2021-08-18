from rest_framework import viewsets, permissions
from .models import Author, Book, Order
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    OrderSerializer,
    UserSerializer,
    User
    )

from rest_framework.authentication import TokenAuthentication


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    authentication_classes = (TokenAuthentication,)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    authentication_classes = (TokenAuthentication,)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    #queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer
