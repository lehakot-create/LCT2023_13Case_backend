from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from main_app.views import ActivateUser, ProfileDetailView


urlpatterns = [
    path('v1/activate/<uid>/<token>', ActivateUser.as_view()),
    path('v1/api-auth/', include('rest_framework.urls',
                                 namespace='rest_framework')),
    url(r'^v1/auth/', include('djoser.urls')),
    url(r'^v1/auth/', include('djoser.urls.authtoken')),
    path('v1/profile/<int:pk>/', ProfileDetailView.as_view()),
]
