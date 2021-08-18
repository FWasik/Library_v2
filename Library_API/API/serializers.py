from rest_framework import serializers
from .models import Order, Book, Author
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['author'] = AuthorSerializer(instance.author).data
        return response


class OrderSerializer(serializers.ModelSerializer):
    '''user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )'''

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = BookSerializer(instance.book).data

        return response

