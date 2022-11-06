import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from django.contrib.postgres.search import SearchQuery, SearchVector

from rest_framework import viewsets, status, authentication
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import settings

from .models import Profile, Project, Stack, Profession, Country, Idea, IdeaComment
from .serializers import (
    ProfileViewSetSerializer,
    StacksSerializer,
    SearchProjectsSerializer,
    GetProjectSerializer,
    ProfessionSerializer,
    CountrySerializer,
    IdeaSerializer,
    CommentSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Представление возвращает все записи из модели Profile

    Возвращает информацию о всех пользователях
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileViewSetSerializer


class ActivateUser(View):
    """
    Класс активации юзера по ссылке, полученной на email
    """
    template_name = "email/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['site_name'] = "Портал инноваций"
        context['protocol'] = 'http'
        context['domain'] = '0.0.0.0:8000'
        context['url'] = settings.ACTIVATION_URL.format(**context)
        return context

    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}
        url = "http://localhost:8000/api/v1/auth/users/activation/"
        response = requests.post(url, data=payload)
        if response.status_code == 204:
            return render(request, "email/activation_complete.html")
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
            return Project.objects.annotate(search=search_vector).filter(search=search_query)


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


class GetUserProjects(ListAPIView):
    """
    Представление возвращает список всех проектов пользователя:
    id, name, description, colour
    """
    queryset = Project.objects.all()
    serializer_class = GetProjectSerializer

    def get_queryset(self):
        user_id = str(self.request.user.id)
        user = Profile.objects.get(pk=user_id)
        return user.profile_project.all()


class ProfessionView(viewsets.ModelViewSet):
    """
    Возвращает список профессий
    """
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class CountryView(viewsets.ModelViewSet):
    """
    Возвращает список стран
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class IdeaView(viewsets.ModelViewSet):
    """
    Возвращает все идеи
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer


class UserIdeaListView(APIView):
    """
    Возвращает идеи пользователя
    """
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def get_queryset(self, pk):
        ideas = Idea.objects.filter(author=pk)
        return ideas

    def get(self, request, pk):
        ideas = self.get_queryset(pk)
        serializer = IdeaSerializer(ideas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserIdeaCreateView(APIView):
    """
    Создает идею
    """
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

    def post(self, request):
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(APIView):
    """
     Возвращает все комменты к данной идее
    """
    def get_queryset(self, pk):
        try:
            comments = IdeaComment.objects.filter(idea=pk)
            return comments
        except IdeaComment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_queryset(pk)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    """
    Создает коммент к идее
    """
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    """
    Возвращает и обновляет профиль по id
    """
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(id=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Возвращает профиль по id
        """
        profile = self.get_object(pk)
        serializer = ProfileViewSetSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Обновляет данные профиля
        params: id
        """
        profile = self.get_object(pk)
        serializer = ProfileViewSetSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
