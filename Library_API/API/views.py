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


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'DELETE', 'PATCH', 'PUT']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        today = date.today()

        diff = abs(today - order.date_order_create.date()).days

        if diff > 1:
            content = {
                'Validation Error': 'Too late to update your order!'
            }

            return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

        order.date_order_create = timezone.now()
        order.date_delivery = today + timedelta(days=2)
        order.rental_end = today + timedelta(days=30)

        #serializer = self.get_serializer(order, data=request.data,
        #                                 partial=True)

        #serializer.is_valid()
        #serializer.save()

        return super(OrderViewSet, self).partial_update(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)
