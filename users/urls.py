from django.urls import path
from .views import *

app_name = "users"
urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("list/", List.as_view(), name="list"),
    path("excluir/<int:pk>/", Excluir.as_view(), name="excluir"),
    path("edit/<int:pk>/", Edit.as_view(), name="edit"),
]
