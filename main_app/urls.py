from django.conf.urls import url
from django.urls import path, include

from main_app.views import ActivateUser, ProfileDetailView, MyTaskView, MyTaskDetailView


urlpatterns = [
    path('v1/activate/<uid>/<token>', ActivateUser.as_view()),
    path('v1/api-auth/', include('rest_framework.urls',
                                 namespace='rest_framework')),
    url(r'^v1/auth/', include('djoser.urls')),
    url(r'^v1/auth/', include('djoser.urls.authtoken')),
    path('v1/profile/<int:pk>/', ProfileDetailView.as_view()),

    path('tasks/', MyTaskView.as_view(), name='task'),
    path('task/<str:pk>', MyTaskDetailView.as_view()),
]
