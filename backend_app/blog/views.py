from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from blog.serializers import BlogOutSerializer
from core.models import Blog
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.viewsets import GenericViewSet


class BlogAPIView(
    DestroyAPIView, 
    RetrieveUpdateAPIView, 
    RetrieveAPIView, 
    ListAPIView, 
    CreateAPIView, 
    GenericViewSet
    ):
    serializer_class = BlogOutSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Blog.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    
