from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required #Permite a exibição de dashboard apenas para logados
from .models import FormLivro, FormCategoria, Livro
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


def login(request):
    if request.method != 'POST':
        return render(request, 'contas/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'contas/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login efetuado com sucesso.')

        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def cadastro(request):
    if request.method != 'POST': # verifica se alguma coisa foi inserida
        return render(request, 'contas/cadastro.html')
    # Não sendo, partimos para atribuição dos valores
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario') # Aqui pegamos todos os inputs de cadastro.html
    senha = request.POST.get('senha')     # colocamos nas devidas variaveis e trabalhamos
    senha2 = request.POST.get('senha2')   # a validação de cada campo

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'É preciso preencher todos os campos!')
        return render(request, 'contas/cadastro.html')

    try:
        validate_email(email) # Verificamos o email com o Django
    except:
        messages.error(request, 'Email inválido') # Caso não valide retornamos para pag. cadastro
        return render(request, 'contas/cadastro.html')
    #Após validação de email, seguimos para validar os demais campos, conforme convenção.

    if len(usuario) < 5:
        messages.error(request, 'Necessário que usuário contenha 5 caracteres ou mais.')
        return render(request, 'contas/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'Necessário que senha tenha 6 caracteres ou mais.')
        return render(request, 'contas/cadastro.html')

    if senha != senha2:
        messages.error(request, 'Senha não confere.')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(username=usuario).exists(): # Com Djando verifica se o usuario já existe
        messages.error(request, 'Usuário já existe, por favor tente outro.')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já cadastrado!') # Com Django verifica se email já é cadastrado
        return render(request, 'contas/cadastro.html')

    # Após passar por todas as verificações o cadastro é realizado

    messages.success(request, 'Cadastro realizado com sucesso!\nLogue abaixo')
    user = User.objects.create_user(username=usuario,
                                    email=email,
                                    password=senha,
                                    first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(login_url='/login/')
def dashboard(request):
    user = request.user
    livros = Livro.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def cadastrar_livro(request):
    if request.method != 'POST':
        form = FormLivro()
        return render(request, 'contas/cadastrar_livro.html', {'form': form})

    form = FormLivro(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar formulário de cadastro.')
        form = FormLivro(request.POST)
        return render(request, 'contas/dashboard.html', {'form': form})

    messages.success(request, f'Livro {request.POST.get("titulo")}  salvo com sucesso!')
    form.save()
    return redirect('dashboard')


@login_required(login_url='/login/')
def busca(request):
    termo = request.GET.get('termo').strip()

    if termo is None or not termo:
        messages.error(request, 'Para pesquisar campo busca não pode ficar vazio.')
        return redirect('dashboard')

    livros = Livro.objects.order_by('-id').filter(
        Q(titulo__icontains=termo) | Q(autor__icontains=termo),
         mostrar=True
         ) # Reune os dados da Class Livro, ordena e armazena na var livros

    if livros is None or not livros:
        messages.error(request, 'Nenhum título ou autor encontrado.')
        return redirect('dashboard')

    paginator = Paginator(livros, 12) # Ref a paginação e quantos iteraveis serão exibidos

    page = request.GET.get('p')
    livros = paginator.get_page(page)
    print(livros)
    print(type(livros))
    return render(request, 'contas/busca.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ver_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    if not livro.mostrar:
        raise Http404()

    return render(request, 'contas/ver_livro.html', {
        'livro': livro
    }) # Retorna e renderiza os iteráveis.


@login_required(login_url='/login/')
def cadastrar_categoria(request):
    if request.method != "POST":
        formulario = FormCategoria
        return render(request, 'contas/cadastrar_categoria.html',
                      {'form': formulario})

    formulario = FormCategoria(request.POST, request.FILES)
    if not formulario.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        formulario = FormCategoria(request.POST)
        return render(request, 'contas/dashboard.hmtl',
                      {'form': formulario})
    messages.success(request, f'Categoria {request.POST.get("nome")} salvo com sucesso!')
    formulario.save()
    return redirect('cadastrar_livro')


def sobre(request):
    return render(request, 'contas/sobre.html')


@login_required(login_url='/login/')
def editor(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    form = FormLivro(instance=livro)

    if request.method != 'POST':
        return render(request, 'contas/editor.html', {'form': form, 'livro': livro})

    form = FormLivro(request.POST, instance=livro)

    if not form.is_valid():
        return render(request, 'contas/sobre.html', {'form': form, 'livro': livro})

    livro.save()
    return redirect('dashboard')


@login_required(login_url='/login/')
def excluir(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    livro.delete()

    return redirect('dashboard')


@login_required(login_url='/login/')
def ordenar_por_titulo(request):
    livros = Livro.objects.order_by('titulo').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ordenar_por_autor(request):
    livros = Livro.objects.order_by('autor').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ordenar_por_editora(request):
    livros = Livro.objects.order_by('editora').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ordenar_por_categoria(request):
    livros = Livro.objects.order_by('categoria').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ordenar_por_estante(request):
    livros = Livro.objects.order_by('estante').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})


@login_required(login_url='/login/')
def ordenar_por_prateleira(request):
    livros = Livro.objects.order_by('prateleira').filter(
        mostrar=True
    )
    paginator = Paginator(livros, 10)

    page = request.GET.get('p')
    livros = paginator.get_page(page)

    return render(request, 'contas/dashboard.html',
                  {'livros': livros})

