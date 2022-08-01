from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Profile, Project
from .serializers import ProfileViewSetSerializer, MostPopularProjectsSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Представление возвращает все записи из модели Profile

    Возвращает информацию о всех пользователях
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileViewSetSerializer

    # Реализовано через декоратор @action. Можно вручную описать json ответ    #
    # """
    #   popular_proj Возвращает json ответ по адресу http://127.0.0.1:8000/api/profile/popular_proj/
    # """
    #
    # @action(methods=['get'], detail=False)
    # def popular_proj(self, request):
    #     popular_proj = Project.objects.order_by('-rating')[:3]
    #     return Response({'popular_proj': [{'name': p.name, 'rating': p.rating} for p in popular_proj]})



class MostPopularProjectsViewSet(viewsets.ModelViewSet):
    """
    Представление возвращает json ответ с 3-мя популярными проектами

    Возвращает json ответ по адресу http://127.0.0.1:8000/api/popular_proj/
    """

    queryset = Project.objects.all()
    serializer_class = MostPopularProjectsSerializer

    def get_queryset(self):
        return Project.objects.order_by('-rating')[:3]
