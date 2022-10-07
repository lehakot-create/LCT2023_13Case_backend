import requests
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Project, Stack, Task
from .serializers import (
    ProfileViewSetSerializer,
    MostPopularProjectsSerializer,
    StacksSerializer,
    SearchProjectsSerializer,
    GetProjectSerializer,
    GetTasksSerializer
)


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
        response = requests.post(url, data=payload)
        if response.status_code == 204:
            return HttpResponse("Профиль успешно активирован!")
        else:
            return HttpResponse(response)


class GetStacks(viewsets.ModelViewSet):
    '''
    Представление возвращает список всех стеков из базы данных
    '''
    queryset = Stack.objects.all()
    serializer_class = StacksSerializer


class FindProjects(viewsets.ModelViewSet):
    '''
    Представление возвращает результат поиска по полям direction (описание проекта) и name (название проекта)
    '''
    queryset = Project.objects.all()
    serializer_class = SearchProjectsSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.split()
            search_query = SearchQuery(value='')
            for q in query:
                search_query |= SearchQuery(value=q)
            search_vector = SearchVector('name', 'direction__name')

            # запрос на поиск проекта по ключевым словам в поле name и direction.
            return Project.objects.annotate(search=search_vector).filter(search=search_query)




#@csrf_exempt # удалить декоратор
class CreateProjectApiView(ListCreateAPIView):
    '''
    Представление возвращает наименование, описание, id и цвет по проекту
    '''

    queryset = Project.objects.all()
    serializer_class = GetProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        id = self.request.GET.get('id')
        if id:
            return Project.objects.filter(pk = int(id))
        return Project.objects.all()


class CreateTaskApiView(ListCreateAPIView):

    queryset = Task.objects.all()
    serializer_class = GetTasksSerializer
    # permission_classes = (AllowAny)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        id = self.request.GET.get('id')
        if id:
            return Task.objects.filter(pk=int(id))
        return Task.objects.all()

    # def post(self, request, *args, **kwargs):
    #     profiles = request.data.get('id')
    #     profiles = request.data.get('status')
    #     profiles = request.data.get('description')
    #     profiles = request.data.get('description')
    #     profiles = request.data.get('project')
    #
    #     return self.create(request, *profiles, *args, **kwargs)