from rest_framework import serializers

from users.models import CustomUser

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role',
        )
        model = CustomUser
