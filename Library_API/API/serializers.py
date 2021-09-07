from rest_framework import serializers
from .models import (Order, Book, Author,
                    Deliverer, Genre, Publisher)


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


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

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
                    raise serializers.ValidationError('Not enough books in library. Try again later.')

        return data
