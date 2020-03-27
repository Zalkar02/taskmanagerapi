from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'register', views.UserCreationSet, 'register')

urlpatterns = [
    path('', include(router.urls))
]
