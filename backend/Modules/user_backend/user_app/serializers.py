from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country']


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        # ['id','username', 'email', 'password', 'phone_number', 'role', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            password=validated_data['password'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        if user.status != 1:
            raise serializers.ValidationError("User account is inactive")

        data['user'] = user
        return data
