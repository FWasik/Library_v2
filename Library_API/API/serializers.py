from rest_framework import serializers
from .models import Order, Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


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
        return response

    def validate(self, data):
        for book_in_order in data['book']:
            book = Book.objects.get(pk=book_in_order.id)

            if book.amount > 0:
                book.amount -= 1
                book.save()

            else:
                raise serializers.ValidationError('Not enough books in library. Try again later.')

        return data
