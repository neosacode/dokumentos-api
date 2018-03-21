from rest_framework import serializers
from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
        	'id', 
        	'last_login', 
        	'username', 
        	'first_name', 
        	'last_name', 
        	'email', 
        	'created', 
        	'modified', 
        	'default_webhook', 
        	'default_pending_message', 
        	'default_valid_message', 
        	'default_invalid_message'
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'password',
            'first_name', 
            'last_name', 
            'email',
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user