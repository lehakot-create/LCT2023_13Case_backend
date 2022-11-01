from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, TokenSerializer

from .models import Profile, Project, Stack, Profession, Country, Idea


class MostPopularProjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'rating')


class StacksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stack
        fields = ('id', 'name',)


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
        fields = ('id', 'name', 'description', 'colour', 'profile')

    def create(self, validated_data):
        user_list = [self.context['request'].auth.user_id]
        new_project = Project(**validated_data)
        new_project.save()
        new_project.profile.set(user_list)
        new_project.save()
        return new_project


class ProfileViewSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'nick_name', 'role',
                  'full_name', 'dateofbirth', 'country', 'citizenship',
                  'gender', 'email', 'agreement',
                  'education', 'employment',
                  'experience', 'achievements', 'profession',
                  'stack', 'role_in_command', 'command', 'status', )
        # fields = "__all__"


# class GetTasksSerializer(serializers.ModelSerializer):
#     profile = ProfileViewSetSerializer(many=True)
#
#     class Meta:
#         model = Task
#         fields = ('id', 'status', 'description', 'profile', 'project')
#
#     def create(self, validated_data):
#         status = validated_data.__getitem__('status')
#         description = validated_data.__getitem__('description')
#         profiles = self.initial_data.get('profile')
#         project = validated_data.__getitem__('project')
#         profile_list = []
#         for profile in profiles:
#             profile_list.append(profile.get('id'))
#         newTask = Task(status=status, description=description, project=project)
#         newTask.save()
#         newTask.profile.set(profile_list)
#         newTask.save()
#         return newTask


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


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


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = '__all__'
