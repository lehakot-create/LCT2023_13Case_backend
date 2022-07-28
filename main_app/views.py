from django.shortcuts import render
from rest_framework import viewsets
from .models import Profile, Project
from .serializers import ProfileViewSetSerializer, MostPopularProjectsSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileViewSetSerializer


class MostPopularProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = MostPopularProjectsSerializer

    def get_queryset(self):
        return Project.objects.order_by('-rating')[:3]
