import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from .models import Profile, Project, Stack
from .serializers import ProfileViewSetSerializer, MostPopularProjectsSerializer, StacksSerializer


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


class ActivateUser(View):
    '''
    Класс активации юзера по ссылке, полученной на email
    '''
    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}
        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data = payload)
        if response.status_code == 204:
            return HttpResponse("Профиль успешно активирован!")
        else:
            return HttpResponse(response)

class GetStacks(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StacksSerializer