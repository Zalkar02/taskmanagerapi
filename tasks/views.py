from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Task, Tag
from .serializer import UserSerializer, TaskSerializer, TagSerializer
from .permissions import IsOwnerOrReadonly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadonly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['tags', 'creation_date', 'finish_date', 'status']                            
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadonly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
