from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Produto


@method_decorator(login_required, name="dispatch")
class Lista(View):
    def get(self, request):
        produtos = Produto.objects.all().order_by("marca")
        return render(request, "estoque_app/lista/index.html", {"produtos": produtos})


@method_decorator(login_required, name="dispatch")
class Adicionar(View):
    def get(self, request):
        return render(request, "estoque_app/form_add/index.html")

    def post(self, request):
        valor = request.POST.get("valor")
        if valor:
            valor = float(valor.replace(",", "."))

        Produto.objects.create(
            nome=request.POST.get("nome"),
            marca=request.POST.get("marca"),
            valor=valor,
            quantidade=request.POST.get("quantidade"),
            imagem=request.FILES.get("imagem"),
        )
        return redirect("estoque:lista")


@method_decorator(login_required, name="dispatch")
class Editar(View):
    def get(self, request, pk):
        produto = get_object_or_404(Produto, id=pk)
        return render(request, "estoque_app/form_edit/index.html", {"produto": produto})

    def post(self, request, pk):
        produto = get_object_or_404(Produto, id=pk)

        valor = request.POST.get("valor")
        if valor:
            produto.valor = float(valor.replace(",", "."))

        quantidade = request.POST.get("quantidade")
        if quantidade:
            produto.quantidade = quantidade

        produto.nome = request.POST.get("nome")
        produto.marca = request.POST.get("marca")

        imagem = request.FILES.get("imagem")
        if imagem:
            if produto.imagem:
                produto.imagem.delete(save=False)
            produto.imagem = imagem

        produto.save()
        return redirect("estoque:lista")


@method_decorator(login_required, name="dispatch")
class Excluir(View):
    def post(self, request, pk):
        produto = get_object_or_404(Produto, id=pk)

        if produto.imagem:
            produto.imagem.delete(save=False)

        produto.delete()
        return redirect("estoque:lista")
