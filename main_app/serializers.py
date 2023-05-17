from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, TokenSerializer

from .models import Profile


class ProfileViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'nick_name', 'role',
                  'full_name', 'dateofbirth', 'country', 'citizenship',
                  'gender', 'email', 'agreement',
                  'education', 'employment',
                  'experience', 'achievements', 'profession',
                  'stack', 'role_in_command', 'command', 'status', )


class MyTokenSerializer(TokenSerializer):
    auth_token = serializers.CharField(source="key")
    id = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = Profile
        fields = (
            'id',
            'auth_token',
            'role',
        )

    def get_id(self, obj):
        user = obj.user
        return user.id

    def get_role(self, obj):
        user = obj.user
        return user.role
