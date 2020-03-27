from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task, Tag
from .serializer import TaskSerializer, TagSerializer, CreateUserSerializer
from .permissions import IsOwnerOrReadOnly

class UserCreationSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['tags__title']
    ordering_fields = ['creation_date', 'finish_date', 'status'] 
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
