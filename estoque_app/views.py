from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Produto
from django.views import View
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class Lista(View):
    def get(self, request):
        produtos = Produto.objects.all().order_by("marca")
        contexto = {"produtos": produtos}
        return render(request, "estoque_app/lista/index.html", contexto)

@method_decorator(login_required, name='dispatch')
class Adicionar(View):
    def get(self, request):
        return render(request, "estoque_app/form_add/index.html")

    def post(self, request):
        nome = request.POST.get("nome")
        marca = request.POST.get("marca")
        valor = request.POST.get("valor")
        if valor:
            valor = float(valor.replace(",", "."))
        quantidade = request.POST.get("quantidade")
        imagem = request.FILES.get("imagem")
        Produto.objects.create(
            nome=nome,
            marca=marca,
            valor=valor,
            quantidade=quantidade,
            imagem=imagem,
        )
        return redirect("estoque:lista")

@method_decorator(login_required, name='dispatch')
class Editar(View):
    def get(self, request, pk):
        produto = Produto.objects.get(id=pk)
        contexto = {"produto": produto}
        return render(request, "estoque_app/form_edit/index.html", contexto)

    def post(self, request, pk):
        produto = Produto.objects.get(id=pk)
        produto.nome = request.POST.get("nome")
        produto.marca = request.POST.get("marca")
        valor = request.POST.get("valor")
        if valor:
            valor = float(valor.replace(",", "."))
            produto.valor = valor
        imagem = request.FILES.get("imagem")
        if imagem:
            if produto.imagem:
                produto.imagem.delete(save=False)
            produto.imagem = imagem
        produto.save()
        return redirect("estoque:lista")

@method_decorator(login_required, name='dispatch')
class Excluir(View):
    def get(self, request, pk):
        produto = Produto.objects.get(id=pk)
        contexto = {"produto": produto}
        return render(request, "estoque_app/confirm_delete/index.html", contexto)

    def post(self, request, pk):
        produto = Produto.objects.get(id=pk)
        produto.delete()
        return redirect("estoque:lista")
