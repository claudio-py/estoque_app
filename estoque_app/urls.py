from django.urls import path
from . import views 
from .views import *

app_name = "estoque"
urlpatterns = [
    path("list/", views.Lista.as_view(), name="lista"),
    path("adicionar/", views.Adicionar.as_view(), name="adicionar"),
    path("editar/<int:pk>/", views.Editar.as_view(), name="editar"),
    path("excluir/<int:pk>/", views.Excluir.as_view(), name="excluir"),
]
