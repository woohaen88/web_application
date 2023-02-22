from django.urls import path
from user import views


app_name = "user"

urlpatterns = [
    path("token/", views.UserCreateTokenView.as_view(), name="token"),
    path("create/", views.UserCreateView.as_view(), name="create"),
]
