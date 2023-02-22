from rest_framework.routers import DefaultRouter
from blog import views
from django.urls import include, path

router = DefaultRouter()
router.register("", views.BlogAPIView)

app_name = "blog"
urlpatterns = [path("", include(router.urls))]
