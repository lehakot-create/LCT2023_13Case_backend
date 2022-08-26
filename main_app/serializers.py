from rest_framework import routers, serializers
from .models import Profile, Project


class ProfileViewSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'nick_name', 'email', 'is_staff', )

class MostPopularProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'rating', )

