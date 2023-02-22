from rest_framework import serializers
from core.models import Blog
from user.serializers import UserOutSerializer


class BlogInSerializer(serializers.ModelSerializer):
    user = UserOutSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "title", "content"]
        read_only_fields = ["id"]


class BlogOutSerializer(BlogInSerializer):
    

    class Meta(BlogInSerializer.Meta):
        fields = BlogInSerializer.Meta.fields + ["updated_at", "created_at"]
