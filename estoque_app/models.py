from django.db import models


# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=10, unique=True)
    valor = models.FloatField()
    quantidade = models.IntegerField()

    def __str__(self):
        # Isso ajuda a mostrar uma informação legível no painel de administração
        return f"{self.nome} {self.marca} {self.valor} ({self.quantidade})"
