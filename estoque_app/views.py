from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Produto
from django.views import View
from django.utils.decorators import method_decorator

# View para listar todos os produtos do estoque
@method_decorator(login_required, name='dispatch')
class Lista(View):
    def get(self, request):
        # Busca todos os produtos ordenados por marca
        produtos = Produto.objects.all().order_by("marca")
        contexto = {"produtos": produtos}
        return render(request, "estoque_app/lista/index.html", contexto)

# View para adicionar um novo produto ao estoque
@method_decorator(login_required, name='dispatch')
class Adicionar(View):
    def get(self, request):
        # Busca todos os produtos ordenados por marca
        return render(request, "estoque_app/form_add/index.html")

    def post(self, request):
        # Processa o formulário de adição de produto
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

# View para editar um produto existente
@method_decorator(login_required, name='dispatch')
class Editar(View):
    def get(self, request, pk):
        # Exibe o formulário de edição com os dados do produto
        produto = Produto.objects.get(id=pk)
        contexto = {"produto": produto}
        return render(request, "estoque_app/form_edit/index.html", contexto)

    def post(self, request, pk):
        # Processa as alterações feitas no produto
        produto = Produto.objects.get(id=pk)
        produto.nome = request.POST.get("nome")
        produto.marca = request.POST.get("marca")
        valor = request.POST.get("valor")
        if valor:
            valor = float(valor.replace(",", "."))
            produto.valor = valor
        imagem = request.FILES.get("imagem")
        if imagem:
            # Remove a imagem antiga antes de salvar a nova
            if produto.imagem:
                produto.imagem.delete(save=False)
            produto.imagem = imagem
        produto.save()
        return redirect("estoque:lista")

# View para excluir um produto do estoque
@method_decorator(login_required, name='dispatch')
class Excluir(View):
    def get(self, request, pk):
        # Exibe a página de confirmação de exclusão
        produto = Produto.objects.get(id=pk)
        contexto = {"produto": produto}
        return render(request, "estoque_app/confirm_delete/index.html", contexto)

    def post(self, request, pk):
        # Remove o produto do banco de dados e exclui a imagem, se houver
        produto = Produto.objects.get(id=pk)
        if produto.imagem:
            produto.imagem.delete(save=False)
        produto.delete()
        return redirect("estoque:lista")
