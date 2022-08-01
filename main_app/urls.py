from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from main_app.views import ProfileViewSet, MostPopularProjectsViewSet

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'popular_proj', MostPopularProjectsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/auth/', include('djoser.urls')),
    url(r'^v1/auth/', include('djoser.urls.authtoken')),
]