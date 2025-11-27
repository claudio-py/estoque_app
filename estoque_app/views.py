from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto


# Create your views here.


def lista(request):
    # 1. Busca todos os objetos 'Carro' no banco de dados
    produtos = Produto.objects.all().order_by("marca")  # Ordena por modelo

    # 2. Cria um "contexto" (um dicionário) para enviar os dados para o HTML
    contexto = {"produtos": produtos}
    # 3. Renderiza o template, passando o contexto
    return render(request, "estoque_app/lista/index.html", contexto)


def adicionar(request):
    if request.method == "POST":
        # pega os dados do formulario
        nome = request.POST.get("nome")
        marca = request.POST.get("marca")
        valor = request.POST.get("valor")
        quantidade = request.POST.get("quantidade")
        # Cria um novo objeto Carro e salva no banco
        Produto.objects.create(
            nome=nome, marca=marca, valor=valor, quantidade=quantidade
        )
        # Redireciona para a lista de carros apos salvar
        return redirect("estoque:lista")
    return render(request, "estoque_app/form_add/index.html")


def editar(request, pk):
    # busca o carro especifico pelo seu id(pk)
    produto = Produto.objects.get(id=pk)

    if request.method == "POST":
        # Atualiza os campos do objeto 'carro' com os dados do formulario
        produto.nome = request.POST.get("nome")
        produto.marca = request.POST.get("marca")
        produto.valor = request.POST.get("valor")
        produto.quantidade = request.POST.get("quantidade")
        produto.save()  ##salva alteracoes
        return redirect("estoque:lista")

    contexto = {"produto": produto}
    return render(request, "estoque_app/form_edit/index.html", contexto)


def excluir(request, pk):
    produto = Produto.objects.get(id=pk)
    if request.method == "POST":  # Se o formulario de confirmacao for enviado
        produto.delete()
        return redirect("estoque:lista")

    contexto = {"produto": produto}
    return render(request, "estoque_app/confirm_delete/index.html", contexto)
