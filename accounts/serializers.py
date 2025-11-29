from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True) 
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já em uso.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data["name"], 
            last_name = validated_data["last_name"],
            email = validated_data["email"], 
            password = validated_data["password"]
        )

        return user