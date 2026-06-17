from django.shortcuts import render

from datetime import date
from urllib.parse import urlencode

from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.urls import reverse


def calcular_idade(data_nascimento):
    hoje = date.today()
    idade = hoje.year - data_nascimento.year

    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade


def inicio(request):
    return render(request, "cadastro/inicio.html")


def cadastro(request):
    contexto = {}

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        data_nascimento_texto = request.POST.get("data_nascimento", "")
        imagem = request.FILES.get("imagem")
        erros = []
        idade = None

        if len(nome) < 3:
            erros.append("O nome deve possuir pelo menos 3 caracteres.")

        if "@" not in email:
            erros.append("O email deve conter o símbolo @.")

        try:
            data_nascimento = date.fromisoformat(data_nascimento_texto)
            idade = calcular_idade(data_nascimento)

            if idade < 18:
                erros.append("A idade deve ser maior ou igual a 18 anos.")
        except ValueError:
            erros.append("Informe uma data de nascimento válida.")

        if erros:
            contexto = {
                "erros": erros,
                "nome": nome,
                "email": email,
                "data_nascimento": data_nascimento_texto,
            }
            return render(request, "cadastro/cadastro.html", contexto)

        nome_imagem = ""

        if imagem:
            fs = FileSystemStorage(location="media")
            nome_imagem = fs.save(imagem.name, imagem)

        parametros = urlencode({
            "nome": nome,
            "email": email,
            "data_nascimento": data_nascimento_texto,
            "idade": idade,
            "imagem": nome_imagem,
        })

        return redirect(f"{reverse('sucesso')}?{parametros}")

    return render(request, "cadastro/cadastro.html", contexto)


def sucesso(request):
    dados = {
        "nome": request.GET.get("nome", ""),
        "email": request.GET.get("email", ""),
        "data_nascimento": request.GET.get("data_nascimento", ""),
        "idade": request.GET.get("idade", ""),
        "imagem": request.GET.get("imagem", ""),
    }

    if not dados["nome"]:
        return redirect("cadastro")

    return render(request, "cadastro/sucesso.html", dados)

