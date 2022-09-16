from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from main_app.views import ProfileViewSet, MostPopularProjectsViewSet, ActivateUser, GetStacks, FindProjects

router = routers.DefaultRouter()
router.register(r'v1/profile', ProfileViewSet)
router.register(r'v1/popular_proj', MostPopularProjectsViewSet)
router.register(r'v1/search', FindProjects, basename='search-projects')
router.register(r'v1/stacks', GetStacks)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/activate/<uid>/<token>', ActivateUser.as_view()),
    path('v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/auth/', include('djoser.urls')),
    url(r'^v1/auth/', include('djoser.urls.authtoken')),
]
