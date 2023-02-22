from django.urls import path, include
from camping import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", views.CampingViewSet)
app_name = "camping"


urlpatterns = [
    path("", include(router.urls)),
]
