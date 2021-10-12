from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True,
                                  max_length=50)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def create(self, validated_data):
        content = ''

        if validated_data['password'] == validated_data['password1']:
            try:
                user = CustomUser.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=validated_data['password'],
                    PESEL=validated_data['PESEL'],
                    phone_number=validated_data['phone_number'],
                    first_name=validated_data['first_name'],
                    middle_name=validated_data['middle_name'],
                    last_name=validated_data['last_name']
                )

                user.save()

                return user

            except KeyError:
                content = {
                    'Validation error': 'All required fields must be filled!'
                }

                raise serializers.ValidationError(content)

        content = {
            'Validation error': 'Passwords not match'
        }
        raise serializers.ValidationError(content)

    class Meta:
        model = CustomUser
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'middle_name', 'last_name']
