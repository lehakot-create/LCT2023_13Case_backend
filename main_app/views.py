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
from rest_framework.generics import get_object_or_404, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import settings

from .models import Profile, Project, Stack, Task, Profession
from .serializers import (
    ProfileViewSetSerializer,
    MostPopularProjectsSerializer,
    StacksSerializer,
    SearchProjectsSerializer,
    GetProjectSerializer,
    GetTasksSerializer,
    ProfessionSerializer,
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
    """
    Класс активации юзера по ссылке, полученной на email
    """
    template_name = "email/activation.html"

    # def get_context_data(self):
    #     context = super().get_context_data()
    #
    #     context['site_name'] = "Портал инноваций"
    #     context['protocol'] = 'http'
    #     context['domain'] = '0.0.0.0:8000'
    #     context['url'] = settings.ACTIVATION_URL.format(**context)
    #     return context

    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}
        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data=payload)
        if response.status_code == 204:
            return HttpResponse("Профиль успешно активирован!")
            # return render(request, "activation.html")
        else:
            return HttpResponse(response)


class GetStacks(viewsets.ModelViewSet):
    """
    Представление возвращает список всех стеков из базы данных
    """
    queryset = Stack.objects.all()
    serializer_class = StacksSerializer


class FindProjects(viewsets.ModelViewSet):
    """
    Представление возвращает результат поиска по полям direction (описание проекта) и name (название проекта)
    """
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


# @csrf_exempt # удалить декоратор
class CreateProjectApiView(ListCreateAPIView):
    """
    Представление возвращает наименование, описание, id и цвет по проекту
    """

    queryset = Project.objects.all()
    serializer_class = GetProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        id = self.request.GET.get('id')
        if id:
            return Project.objects.filter(pk=int(id))
        return Project.objects.all()


class CreateTaskApiView(ListCreateAPIView):
    """
    Представление возвращает наименование, описание и цвет проекта по его id
    """
    queryset = Task.objects.all()
    serializer_class = GetTasksSerializer

    # permission_classes = (AllowAny)Project.objects.values_list('members')alues_list('members')

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        id = self.request.GET.get('id')
        if id:
            return Task.objects.filter(pk=int(id))
        return Task.objects.all()


class GetUserProjects(ListAPIView):
    """
    Представление возвращает список всех проектов пользователя:
    id, name, description, colour
    """
    queryset = Project.objects.all()
    serializer_class = GetProjectSerializer

    def get_queryset(self):
        # Получил из запроса id пользователя по токену
        user_id = str(self.request.user.id)
        # Создал объект пользователя по полученному id
        user = Profile.objects.get(pk=user_id)
        # profile_project - это промежуточная таблица (название указано в related_name)
        # у объекта получаю список всех проектов через промежуточную таблицу
        return user.profile_project.all()


class ProfessionView(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
