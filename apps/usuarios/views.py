from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from apps.receitas.models import Receita


def cadastro(request):
    """ Cadastra um novo usuario no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode estar em branco')
            return redirect('cadastro')
        email = request.POST['email']
        if campo_vazio(email):
            messages.error(request, 'O campo email não pode estar em branco')
            return redirect('cadastro')
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuario já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuario já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'login realizado com sucesso!')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_authenticated:
        pessoa_id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=pessoa_id)

        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2
