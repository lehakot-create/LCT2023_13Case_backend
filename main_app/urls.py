from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from main_app.views import (ProfileViewSet,
    # MostPopularProjectsViewSet,
                            ActivateUser,
                            GetStacks,
                            FindProjects,
                            CreateProjectApiView,
    # CreateTaskApiView,
                            GetUserProjects,
                            ProfessionView, CountryView, IdeaView, UserIdeaListView, CommentListView, ProfileDetailView,
                            )

router = routers.DefaultRouter()
#router.register(r'v1/profile', ProfileViewSet)
# router.register(r'v1/popular_proj', MostPopularProjectsViewSet)
router.register(r'v1/search', FindProjects)
router.register(r'v1/stacks', GetStacks)
router.register(r'v1/profession', ProfessionView)
router.register(r'v1/country', CountryView)
router.register(r'v1/all_ideas', IdeaView)
# router.register(r'v1/user_ideas', UserIdeaView)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/activate/<uid>/<token>', ActivateUser.as_view()),
    path('v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/project/', CreateProjectApiView.as_view()),
    # path('v1/tasks/', CreateTaskApiView.as_view()),
    # path('v1/user-projects/', GetUserProjects.as_view()),
    url(r'^v1/auth/', include('djoser.urls')),
    url(r'^v1/auth/', include('djoser.urls.authtoken')),
    path('v1/user_ideas/<int:pk>/', UserIdeaListView.as_view()),
    path('v1/comment/<int:pk>/', CommentListView.as_view()),
    path('v1/profile/<int:pk>/', ProfileDetailView.as_view()),
    # path('v1/user_idea/<int:pk>/', UserIdeaDetailView.as_view()),
]
