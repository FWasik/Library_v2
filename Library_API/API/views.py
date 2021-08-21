from rest_framework import viewsets, permissions, serializers
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
    authentication_classes = (TokenAuthentication,)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Book.objects.all()
    authentication_classes = (TokenAuthentication,)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        book_data = self.request.data['book']
        book = Book.objects.get(pk=book_data)
        if book.amount > 0:
            book.amount -= 1
            if serializer.is_valid():
                serializer.save(user=self.request.user)
        else:
           raise serializers.ValidationError('Not enough books in library. Try again later.')

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user=user)
