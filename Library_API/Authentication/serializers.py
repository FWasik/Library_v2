from rest_framework import serializers
from .models import CustomUser
from django.core.validators import RegexValidator


validator_password = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,30}$"


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,
                                     validators=[RegexValidator(regex=validator_password,
                                                                message="Zły format hasła!")])
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

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
                raise serializers.ValidationError({
                    'Validation error': ['Wszystkie potrzebne pola muszą być wypełnione!']
                })

        raise serializers.ValidationError({
            'Validation error': ['Hasła nie pasują!']
        })

    def update(self, instance, validated_data):

        if validated_data.__contains__('password'):
            if validated_data['password'] != validated_data['password1']:
                raise serializers.ValidationError({'Validation error': ['Hasła nie pasują!']})

            user = instance
            if not user.check_password(validated_data['old_password']):
                raise serializers.ValidationError({'Validation error': ['Niepoprawne stare hasło']})

            instance.set_password(validated_data['password'])
            instance.save()

            return instance

        else:
            if validated_data.__contains__('image') and not instance.image.name == 'default.jpg':
                instance.image.delete()

            for (key, value) in validated_data.items():
                setattr(instance, key, value)

            instance.save()

            return instance
