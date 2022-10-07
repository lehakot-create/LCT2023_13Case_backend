from rest_framework import routers, serializers
from .models import Profile, Project, Stack, Task





class MostPopularProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'rating')


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


class ProfileViewSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','nick_name')
class GetTasksSerializer(serializers.ModelSerializer):
    profile = ProfileViewSetSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'status', 'description', 'profile', 'project')

    def create(self, validated_data):
        status = validated_data.__getitem__('status')
        description = validated_data.__getitem__('description')
        profiles = self.initial_data.get('profile')
        project = validated_data.__getitem__('project')
        profile_list = []
        for profile in profiles:
            profile_list.append(profile.get('id'))
        newTask = Task(status=status, description=description, project=project)
        newTask.save()
        newTask.profile.set(profile_list)
        newTask.save()
        return newTask