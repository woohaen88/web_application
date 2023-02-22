from core.models import Camping

from rest_framework import serializers

from user.serializers import UserOutSerializer


class CampingInSerializer(serializers.ModelSerializer):
    user = UserOutSerializer(read_only=True)

    class Meta:
        model = Camping
        fields = "__all__"
        read_only_fields = ["id", "updated_at", "created_at"]


class CampingOutSerializer(CampingInSerializer):
    pass
