import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import settings

from .models import Profile
from .serializers import ProfileViewSetSerializer


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
