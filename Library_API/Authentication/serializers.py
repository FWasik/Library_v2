from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True,
                                  max_length=50)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            PESEL=validated_data['PESEL'],
            phone_number=validated_data['phone_number']
        )

        user.save()

        return user

    class Meta:
        model = CustomUser
        fields = '__all__'
