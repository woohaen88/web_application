from rest_framework.viewsets import ModelViewSet
from camping.serializers import CampingInSerializer, CampingOutSerializer
from core.models import Camping
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.generics import GenericAPIView


class CampingViewSet(ModelViewSet, GenericAPIView):
    serializer_class = CampingInSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Camping.objects.all()
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_serializer_class(self):
        if self.action == "list":
            return CampingOutSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
