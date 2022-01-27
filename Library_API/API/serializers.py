from rest_framework import serializers
from .models import (Order, Book, Author,
                     Deliverer, Genre, Publisher, Address)

from django.core.exceptions import ObjectDoesNotExist


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class DelivererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverer
        fields = '__all__'


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
        response['author'] = AuthorSerializer(instance.author.all(), many=True).data
        response['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        response['publisher'] = PublisherSerializer(instance.publisher).data
        return response


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['book'] = BookSerializer(instance.book.all(), many=True).data
        response['deliverer'] = DelivererSerializer(instance.deliverer).data
        return response

    def validate(self, data):
        if 'book' in data:
            for book_in_order in data['book']:
                book = Book.objects.get(pk=book_in_order.id)

                if book.amount > 0:
                    book.amount -= 1
                    book.save()

                else:
                    content = {
                        'Validation_error': 'Brak książki ' + book.title + '!'
                    }
                    raise serializers.ValidationError(content)

        return data

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        deliverer_data = validated_data.pop('deliverer')
        book_data = validated_data.pop('book')
        user_data = validated_data.pop('user')

        try:
            address = Address.objects.get(**address_data)
        except ObjectDoesNotExist:
            address = Address.objects.create(**address_data)

        order = Order.objects.create(address=address,
                                     deliverer=deliverer_data,
                                     user=user_data)
        order.book.add(*book_data)

        return order
