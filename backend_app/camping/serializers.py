from core.models import Camping, CampingTag

from rest_framework import serializers

from user.serializers import UserOutSerializer


class TagInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampingTag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagOutSerializer(TagInSerializer):
    class Meta(TagInSerializer.Meta):
        fields = TagInSerializer.Meta.fields + ["slug"]
        read_only_fields = TagInSerializer.Meta.read_only_fields + ["slug"]


class CampingInSerializer(serializers.ModelSerializer):
    user = UserOutSerializer(read_only=True)
    tags = TagOutSerializer(required=False, many=True)

    class Meta:
        model = Camping
        fields = "__all__"
        read_only_fields = ["id", "updated_at", "created_at"]


class CampingOutSerializer(CampingInSerializer):
    pass
