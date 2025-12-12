from django.db import models


# Modelos do aplicativo de estoque
class Produto(models.Model):
    nome = models.CharField(max_length=30)
    marca = models.CharField(max_length=30)
    valor = models.FloatField()
    quantidade = models.IntegerField()
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    def __str__(self):
        # Isso ajuda a mostrar uma informação legível no painel de administração
        return f"{self.nome} {self.marca} {self.valor} ({self.quantidade})"
