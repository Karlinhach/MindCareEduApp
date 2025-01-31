from pyexpat.errors import messages
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Administrador, Emocoes, Relatorios, Organization, Server
from .forms import AddressForm, OrganizationForm, StudentForm, ServerForm
import json

class AdministradorListView(ListView):
    model = Administrador
    template_name = 'administrador_list.html'

class AdministradorDetailView(DetailView):
    model = Administrador
    template_name = 'administrador_detail.html'

class AdministradorCreateView(CreateView):
    model = Administrador
    template_name = 'administrador_form.html'
    fields = ['nome', 'contatos', 'email', 'sexo', 'senha']
    success_url = reverse_lazy('administrador-list')

class AdministradorUpdateView(UpdateView):
    model = Administrador
    template_name = 'administrador_form.html'
    fields = ['nome', 'contatos', 'email', 'sexo', 'senha']
    success_url = reverse_lazy('administrador-list')

class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'administrador_confirm_delete.html'
    success_url = reverse_lazy('administrador-list')

class EmocoesListView(ListView):
    model = Emocoes
    template_name = 'emocoes_list.html'

class RelatoriosListView(ListView):
    model = Relatorios
    template_name = 'relatorios_list.html'


#LOGINs

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("password")

        # Verifica se é um Administrador
        administrador = Administrador.objects.filter(email=email).first()
        if administrador and administrador.senha == senha:
            request.session['user_id'] = administrador.id_adm
            request.session['user_type'] = 'admin'
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home')
        
        # Verifica se é um Servidor
        servidor = Server.objects.filter(email=email).first()
        if servidor and servidor.password == senha:
            request.session['user_id'] = servidor.id
            request.session['user_type'] = 'server'
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home')  

        messages.error(request, "Credenciais inválidas. Tente novamente.")
    
    return render(request, "login.html")

#Proteção view
def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_type' not in request.session:
            return HttpResponseForbidden("Acesso negado")
        return view_func(request, *args, **kwargs)
    return wrapper

# View para listar as organizações
def list_organizations(request):
    organizations = Organization.objects.all()
    return render(request, 'list_organizations.html', {'organizations': organizations})

@csrf_exempt
def create_organization(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        organization_form = OrganizationForm(request.POST)
        
        if address_form.is_valid() and organization_form.is_valid():
            # Salva o endereço
            address = address_form.save()
            organization = organization_form.save(commit=False)
            organization.address = address
            organization.save()

            return redirect('list_organizations')
        else:
            # Exibe erros de formulário para depuração
            print(address_form.errors)
            print(organization_form.errors)
    
    else:
        address_form = AddressForm()
        organization_form = OrganizationForm()

    return render(request, 'create_organization.html', {
        'address_form': address_form,
        'organization_form': organization_form,
    })


@csrf_exempt
def student_create(request):
    organizations = Organization.objects.filter(active=True)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        print(request.POST)  # Verifique o conteúdo dos dados enviados
        if form.is_valid():
            form.save()
            return redirect('student_list')
        else:
            print(form.errors)  # Exibe os erros de validação
    else:
        form = StudentForm()
    return render(request, 'student_create.html', {'form': form, 'organizations': organizations})

def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ServerForm()
    # Obtém a lista de organizações para exibir no select do formulário
    organizations = Organization.objects.all()

    return render(request, 'create_servidor.html', {'form': form, 'organizations': organizations})



@csrf_exempt
def cadastro(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        contatos = request.POST.get('contatos')
        email = request.POST.get('email')
        sexo = request.POST.get('sexo')
        senha = request.POST.get('password')

        # Validar campos básicos (adapte conforme necessário)
        if not nome or not email or not senha:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect('cadastro.html')

        # Verifica se o e-mail já está em uso
        if Administrador.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return redirect('cadastro.html')

        # Criar novo administrador
        administrador = Administrador(
            nome=nome,
            contatos=contatos,
            email=email,
            sexo=sexo,
            senha=senha,  #Utilize hashing para senhas
        )
        administrador.save()

        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('login.html')  # Substitua pelo nome da página de login ou outra página

    return render(request, 'cadastro.html')

@csrf_exempt
def receber_emocoes(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        emocao = Emocoes(
            matricula_id=dados['matricula'],
            descricao=dados['descricao'],
            emocao_detectada=dados['emocao_detectada'],
            data_hora=dados['data_hora'],
            confianca=dados['confianca'],
            foto=dados['foto'],
        )
        emocao.save()
        return JsonResponse({'status': 'Emoção recebida e armazenada com sucesso'})

@csrf_exempt
def receber_relatorios(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        relatorio = Relatorios(
            matricula_id=dados['matricula'],
            id_emocao_id=dados['id_emocao'],
            emocao_detectada=dados['emocao_detectada'],
            relatorio=dados['relatorio'],
            data_hora=dados['data_hora'],
        )
        relatorio.save()
        return JsonResponse({'status': 'Relatório recebido e armazenado com sucesso'})

def home(request):
    user_type = request.session.get('user_type')  # Pode ser 'admin' ou 'server'
    return render(request, "home.html", {'user_type': user_type})

def base_view(request):
    user_type = request.session.get('user_type')
    return render(request, 'base.html', {'user_type': user_type})
