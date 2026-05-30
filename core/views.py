from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import (
    Exercicio, PlanejamentoSemanal, AtividadeDiaria, MetaSemanal,
    Anotacao, HistoricoAtividade, CategoriaExercicio, GrupoMuscular
)
from .forms import (
    UserRegisterForm, ExercicioForm, PlanejamentoSemanalForm,
    AtividadeDiariaForm, MetaSemanalForm, AnotacaoForm,
    CategoriaExercicioForm, GrupoMuscularForm
)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo ao FitRoutine.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def dashboard(request):
    hoje = date.today()
    dia_semana = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM'][hoje.weekday()]
    
    planejamento_ativo = PlanejamentoSemanal.objects.filter(usuario=request.user, ativo=True).first()
    treinos_hoje = []
    if planejamento_ativo:
        treinos_hoje = AtividadeDiaria.objects.filter(planejamento=planejamento_ativo, dia_semana=dia_semana).order_by('horario')
    
    meta_atual = MetaSemanal.objects.filter(usuario=request.user, data_inicio__lte=hoje, data_fim__gte=hoje).first()
    ultimas_anotacoes = Anotacao.objects.filter(usuario=request.user).order_by('-data', '-id')[:3]
    
    context = {
        'planejamento_ativo': planejamento_ativo,
        'treinos_hoje': treinos_hoje,
        'meta_atual': meta_atual,
        'ultimas_anotacoes': ultimas_anotacoes,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def exercicios_list(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'core/exercicios.html', {'exercicios': exercicios})

@login_required
def exercicio_create(request):
    if request.method == 'POST':
        form = ExercicioForm(request.POST)
        if form.is_valid():
            exercicio = form.save(commit=False)
            exercicio.criado_por = request.user
            exercicio.save()
            messages.success(request, 'Exercício cadastrado com sucesso!')
            return redirect('exercicios')
    else:
        form = ExercicioForm()
    return render(request, 'core/exercicio_form.html', {'form': form})

@login_required
def planejamento_list(request):
    planejamentos = PlanejamentoSemanal.objects.filter(usuario=request.user).order_by('-data_inicio')
    return render(request, 'core/planejamento.html', {'planejamentos': planejamentos})

@login_required
def planejamento_create(request):
    if request.method == 'POST':
        form = PlanejamentoSemanalForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.usuario = request.user
            if plan.ativo:
                PlanejamentoSemanal.objects.filter(usuario=request.user).update(ativo=False)
            plan.save()
            messages.success(request, 'Planejamento criado com sucesso!')
            return redirect('planejamento_detail', pk=plan.pk)
    else:
        form = PlanejamentoSemanalForm()
    return render(request, 'core/planejamento_form.html', {'form': form})

@login_required
def planejamento_detail(request, pk):
    planejamento = get_object_or_404(PlanejamentoSemanal, pk=pk, usuario=request.user)
    atividades = AtividadeDiaria.objects.filter(planejamento=planejamento).order_by('horario')
    
    if request.method == 'POST':
        form = AtividadeDiariaForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.planejamento = planejamento
            atividade.save()
            messages.success(request, 'Atividade adicionada com sucesso!')
            return redirect('planejamento_detail', pk=pk)
    else:
        form = AtividadeDiariaForm()
        
    context = {
        'planejamento': planejamento,
        'atividades': atividades,
        'form': form
    }
    return render(request, 'core/planejamento_detail.html', context)

@login_required
def calendario(request):
    planejamento_ativo = PlanejamentoSemanal.objects.filter(usuario=request.user, ativo=True).first()
    atividades = {}
    if planejamento_ativo:
        todas_atividades = AtividadeDiaria.objects.filter(planejamento=planejamento_ativo).order_by('horario')
        for dia in [d[0] for d in AtividadeDiaria.DIAS_DA_SEMANA]:
            atividades[dia] = [a for a in todas_atividades if a.dia_semana == dia]
            
    return render(request, 'core/calendario.html', {'planejamento_ativo': planejamento_ativo, 'atividades': atividades})

@login_required
def marcar_concluida(request, pk):
    atividade = get_object_or_404(AtividadeDiaria, pk=pk, planejamento__usuario=request.user)
    atividade.concluida = not atividade.concluida
    atividade.save()
    
    if atividade.concluida:
        HistoricoAtividade.objects.create(
            usuario=request.user,
            atividade=atividade,
            data_realizada=date.today(),
            duracao_real=atividade.duracao
        )
        messages.success(request, 'Atividade marcada como concluída!')
    else:
        HistoricoAtividade.objects.filter(usuario=request.user, atividade=atividade, data_realizada=date.today()).delete()
        messages.info(request, 'Atividade desmarcada.')
        
    return redirect(request.META.get('HTTP_REFERER', 'calendario'))

@login_required
def metas_list(request):
    metas = MetaSemanal.objects.filter(usuario=request.user).order_by('-data_inicio')
    return render(request, 'core/metas.html', {'metas': metas})

@login_required
def meta_create(request):
    if request.method == 'POST':
        form = MetaSemanalForm(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.usuario = request.user
            meta.save()
            messages.success(request, 'Meta criada com sucesso!')
            return redirect('metas')
    else:
        form = MetaSemanalForm()
    return render(request, 'core/meta_form.html', {'form': form})

@login_required
def historico_list(request):
    historico = HistoricoAtividade.objects.filter(usuario=request.user).order_by('-data_realizada', '-registrado_em')
    return render(request, 'core/historico.html', {'historico': historico})

@login_required
def anotacoes_list(request):
    anotacoes = Anotacao.objects.filter(usuario=request.user).order_by('-data', '-id')
    return render(request, 'core/anotacoes.html', {'anotacoes': anotacoes})

@login_required
def anotacao_create(request):
    if request.method == 'POST':
        form = AnotacaoForm(request.POST)
        if form.is_valid():
            anotacao = form.save(commit=False)
            anotacao.usuario = request.user
            anotacao.save()
            messages.success(request, 'Anotação salva com sucesso!')
            return redirect('anotacoes')
    else:
        form = AnotacaoForm()
    return render(request, 'core/anotacao_form.html', {'form': form})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaExercicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('dashboard')
    else:
        form = CategoriaExercicioForm()
    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Nova Categoria'})

@login_required
def grupo_create(request):
    if request.method == 'POST':
        form = GrupoMuscularForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo Muscular criado com sucesso!')
            return redirect('dashboard')
    else:
        form = GrupoMuscularForm()
    return render(request, 'core/grupo_form.html', {'form': form, 'title': 'Novo Grupo Muscular'})
