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
    description = serializers.ReadOnlyField()
    deadline = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ('name', 'description', 'deadline',)

class GetProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    colour = serializers.CharField()

    class Meta:
        model = Project
        fields = ('id','name', 'description', 'colour')

    def create(self, validated_data):
        return Project.objects.create(**validated_data)