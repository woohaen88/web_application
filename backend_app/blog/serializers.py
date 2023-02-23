from rest_framework import serializers
from core.models import Blog, BlogTag
from user.serializers import UserOutSerializer


class TagInSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagOutSerializer(TagInSerializer):
    class Meta(TagInSerializer.Meta):
        fields = TagInSerializer.Meta.fields + ["slug"]
        read_only_fields = TagInSerializer.Meta.read_only_fields + ["slug"]


class BlogInSerializer(serializers.ModelSerializer):
    user = UserOutSerializer(read_only=True)
    tags = TagOutSerializer(required=False, many=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "content"]
        read_only_fields = ["id"]


class BlogOutSerializer(BlogInSerializer):
    class Meta(BlogInSerializer.Meta):
        fields = BlogInSerializer.Meta.fields + ["updated_at", "created_at"]
