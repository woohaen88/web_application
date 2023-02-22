from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


class UserInSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ["password"]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={
            "input_type": "password",
        },
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(self.context.get("request"), email=email, password=password)
        if user is None:
            msg = "유저 인증 실패!!"
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return super().validate(attrs)
