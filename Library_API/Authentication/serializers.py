from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                     validators=[RegexValidator(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,30}$",
                                                                message="Zły format hasła!")])
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        content = ''

        if validated_data['password'] == validated_data['password1']:
            try:
                #username = validated_data['username']

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
                #user = CustomUser.objects.get_by_natural_key(username)
                #Token.objects.create(user=user)
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

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        if validated_data.__contains__('image'):
            instance.image.delete()

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

'''
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'middle_name', 'last_name']
'''