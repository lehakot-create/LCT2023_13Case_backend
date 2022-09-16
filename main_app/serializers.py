from rest_framework import routers, serializers
from .models import Profile, Project, Stack


class ProfileViewSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'nick_name', 'email', 'is_staff',)


class MostPopularProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'rating',)


class StacksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stack
        fields = ('name',)


class SearchProjectsSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    direction = serializers.ReadOnlyField(source='direction.name')
    deadline = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ('name', 'direction', 'deadline',)
