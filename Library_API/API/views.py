from rest_framework import viewsets, permissions
from .models import (Author, Book, Order,
                     Publisher, Genre, Deliverer, Address)
from .serializers import (AuthorSerializer, BookSerializer,
                          OrderSerializer, PublisherSerializer,
                          GenreSerializer, DelivererSerializer,
                          AddressSerializer)
from datetime import timedelta, date
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


#Permission for some methods
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff



class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class PublisherViewSet(viewsets.ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class DelivererViewSet(viewsets.ModelViewSet):
    serializer_class = DelivererSerializer
    queryset = Deliverer.objects.all()

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


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'DELETE', 'PATCH', 'PUT']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'DELETE']:
            return [IsOwnerOrAdmin()]

        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

        return [permissions.IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        today = date.today()

        diff = abs(today - order.date_order_create.date()).days

        if diff > 1:
            content = {
                "Error": "Too late to delete order!"
            }

            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        address = order.address

        orders_temp = list(filter(lambda ord: ord != order, list(Order.objects.all())))
        orders = list(filter(lambda order: order.address == address, orders_temp))

        if not orders:
            address.delete()

        books = order.book.all()

        for book in books:
            book.amount += 1
            book.save()

        return super(OrderViewSet, self).destroy(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)
