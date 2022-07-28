from rest_framework import routers, serializers
from .models import Profile, Project


class ProfileViewSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'username', 'email', 'is_staff', )

class MostPopularProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'rating', )

