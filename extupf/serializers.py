from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'avatar', 'phone')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
