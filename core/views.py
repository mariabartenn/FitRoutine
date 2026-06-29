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
    CategoriaExercicioForm, GrupoMuscularForm, HistoricoAtividadeForm
)


# ---------------------------------------------------------------------------
# PÁGINAS GERAIS
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 1. EXERCÍCIOS
# ---------------------------------------------------------------------------

@login_required
def exercicios_list(request):
    exercicios = Exercicio.objects.all().order_by('nome')
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
    return render(request, 'core/exercicio_form.html', {'form': form, 'title': 'Novo Exercício'})


@login_required
def exercicio_update(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    if request.method == 'POST':
        form = ExercicioForm(request.POST, instance=exercicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercício atualizado com sucesso!')
            return redirect('exercicios')
    else:
        form = ExercicioForm(instance=exercicio)
    return render(request, 'core/exercicio_form.html', {'form': form, 'title': 'Editar Exercício'})


@login_required
def exercicio_delete(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    if request.method == 'POST':
        exercicio.delete()
        messages.success(request, 'Exercício excluído com sucesso!')
        return redirect('exercicios')
    return render(request, 'core/confirm_delete.html', {'objeto': exercicio, 'voltar': 'exercicios'})


# ---------------------------------------------------------------------------
# 2. CATEGORIAS DE EXERCÍCIO
# ---------------------------------------------------------------------------

@login_required
def categorias_list(request):
    categorias = CategoriaExercicio.objects.all().order_by('nome')
    return render(request, 'core/categorias.html', {'categorias': categorias})


@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaExercicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('categorias')
    else:
        form = CategoriaExercicioForm()
    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Nova Categoria'})


@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(CategoriaExercicio, pk=pk)
    if request.method == 'POST':
        form = CategoriaExercicioForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('categorias')
    else:
        form = CategoriaExercicioForm(instance=categoria)
    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Editar Categoria'})


@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(CategoriaExercicio, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
        return redirect('categorias')
    return render(request, 'core/confirm_delete.html', {'objeto': categoria, 'voltar': 'categorias'})


# ---------------------------------------------------------------------------
# 3. GRUPOS MUSCULARES
# ---------------------------------------------------------------------------

@login_required
def grupos_list(request):
    grupos = GrupoMuscular.objects.all().order_by('nome')
    return render(request, 'core/grupos.html', {'grupos': grupos})


@login_required
def grupo_create(request):
    if request.method == 'POST':
        form = GrupoMuscularForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo Muscular criado com sucesso!')
            return redirect('grupos')
    else:
        form = GrupoMuscularForm()
    return render(request, 'core/grupo_form.html', {'form': form, 'title': 'Novo Grupo Muscular'})


@login_required
def grupo_update(request, pk):
    grupo = get_object_or_404(GrupoMuscular, pk=pk)
    if request.method == 'POST':
        form = GrupoMuscularForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo Muscular atualizado com sucesso!')
            return redirect('grupos')
    else:
        form = GrupoMuscularForm(instance=grupo)
    return render(request, 'core/grupo_form.html', {'form': form, 'title': 'Editar Grupo Muscular'})


@login_required
def grupo_delete(request, pk):
    grupo = get_object_or_404(GrupoMuscular, pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Grupo Muscular excluído com sucesso!')
        return redirect('grupos')
    return render(request, 'core/confirm_delete.html', {'objeto': grupo, 'voltar': 'grupos'})


# ---------------------------------------------------------------------------
# 4. PLANEJAMENTO SEMANAL (+ ATIVIDADES DIÁRIAS via inline na página)
# ---------------------------------------------------------------------------

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
    return render(request, 'core/planejamento_form.html', {'form': form, 'title': 'Novo Planejamento'})


@login_required
def planejamento_update(request, pk):
    plan = get_object_or_404(PlanejamentoSemanal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PlanejamentoSemanalForm(request.POST, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            if plan.ativo:
                PlanejamentoSemanal.objects.filter(usuario=request.user).exclude(pk=plan.pk).update(ativo=False)
            plan.save()
            messages.success(request, 'Planejamento atualizado com sucesso!')
            return redirect('planejamento_detail', pk=plan.pk)
    else:
        form = PlanejamentoSemanalForm(instance=plan)
    return render(request, 'core/planejamento_form.html', {'form': form, 'title': 'Editar Planejamento'})


@login_required
def planejamento_delete(request, pk):
    plan = get_object_or_404(PlanejamentoSemanal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Planejamento excluído com sucesso!')
        return redirect('planejamentos')
    return render(request, 'core/confirm_delete.html', {'objeto': plan, 'voltar': 'planejamentos'})


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


# ---------------------------------------------------------------------------
# 5. ATIVIDADES DIÁRIAS (editar/excluir individualmente)
# ---------------------------------------------------------------------------

@login_required
def atividade_update(request, pk):
    atividade = get_object_or_404(AtividadeDiaria, pk=pk, planejamento__usuario=request.user)
    if request.method == 'POST':
        form = AtividadeDiariaForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada com sucesso!')
            return redirect('planejamento_detail', pk=atividade.planejamento.pk)
    else:
        form = AtividadeDiariaForm(instance=atividade)
    return render(request, 'core/atividade_form.html', {'form': form, 'title': 'Editar Atividade', 'atividade': atividade})


@login_required
def atividade_delete(request, pk):
    atividade = get_object_or_404(AtividadeDiaria, pk=pk, planejamento__usuario=request.user)
    plan_pk = atividade.planejamento.pk
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade excluída com sucesso!')
        return redirect('planejamento_detail', pk=plan_pk)
    return render(request, 'core/confirm_delete.html', {'objeto': atividade, 'voltar': 'planejamento_detail', 'voltar_pk': plan_pk})


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


# ---------------------------------------------------------------------------
# 6. CALENDÁRIO
# ---------------------------------------------------------------------------

@login_required
def calendario(request):
    planejamento_ativo = PlanejamentoSemanal.objects.filter(usuario=request.user, ativo=True).first()
    atividades = {}
    if planejamento_ativo:
        todas_atividades = AtividadeDiaria.objects.filter(planejamento=planejamento_ativo).order_by('horario')
        for dia in [d[0] for d in AtividadeDiaria.DIAS_DA_SEMANA]:
            atividades[dia] = [a for a in todas_atividades if a.dia_semana == dia]

    return render(request, 'core/calendario.html', {'planejamento_ativo': planejamento_ativo, 'atividades': atividades})


# ---------------------------------------------------------------------------
# 7. METAS SEMANAIS
# ---------------------------------------------------------------------------

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
    return render(request, 'core/meta_form.html', {'form': form, 'title': 'Nova Meta'})


@login_required
def meta_update(request, pk):
    meta = get_object_or_404(MetaSemanal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MetaSemanalForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meta atualizada com sucesso!')
            return redirect('metas')
    else:
        form = MetaSemanalForm(instance=meta)
    return render(request, 'core/meta_form.html', {'form': form, 'title': 'Editar Meta'})


@login_required
def meta_delete(request, pk):
    meta = get_object_or_404(MetaSemanal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        meta.delete()
        messages.success(request, 'Meta excluída com sucesso!')
        return redirect('metas')
    return render(request, 'core/confirm_delete.html', {'objeto': meta, 'voltar': 'metas'})


@login_required
def meta_concluir(request, pk):
    meta = get_object_or_404(MetaSemanal, pk=pk, usuario=request.user)
    meta.concluida = not meta.concluida
    meta.save()
    if meta.concluida:
        messages.success(request, 'Meta marcada como concluída!')
    else:
        messages.info(request, 'Meta marcada como pendente.')
    return redirect('metas')


# ---------------------------------------------------------------------------
# 8. ANOTAÇÕES
# ---------------------------------------------------------------------------

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
    return render(request, 'core/anotacao_form.html', {'form': form, 'title': 'Nova Anotação'})


@login_required
def anotacao_update(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AnotacaoForm(request.POST, instance=anotacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anotação atualizada com sucesso!')
            return redirect('anotacoes')
    else:
        form = AnotacaoForm(instance=anotacao)
    return render(request, 'core/anotacao_form.html', {'form': form, 'title': 'Editar Anotação'})


@login_required
def anotacao_delete(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        anotacao.delete()
        messages.success(request, 'Anotação excluída com sucesso!')
        return redirect('anotacoes')
    return render(request, 'core/confirm_delete.html', {'objeto': anotacao, 'voltar': 'anotacoes'})


# ---------------------------------------------------------------------------
# 9. HISTÓRICO DE ATIVIDADES
# ---------------------------------------------------------------------------

@login_required
def historico_list(request):
    historico = HistoricoAtividade.objects.filter(usuario=request.user).order_by('-data_realizada', '-registrado_em')
    return render(request, 'core/historico.html', {'historico': historico})


@login_required
def historico_create(request):
    qs_atividades = AtividadeDiaria.objects.filter(planejamento__usuario=request.user)
    if request.method == 'POST':
        form = HistoricoAtividadeForm(request.POST)
        form.fields['atividade'].queryset = qs_atividades
        if form.is_valid():
            historico = form.save(commit=False)
            historico.usuario = request.user
            historico.save()
            messages.success(request, 'Registro de histórico adicionado com sucesso!')
            return redirect('historico')
    else:
        form = HistoricoAtividadeForm()
        form.fields['atividade'].queryset = qs_atividades
    return render(request, 'core/historico_form.html', {'form': form, 'title': 'Novo Registro de Histórico'})


@login_required
def historico_delete(request, pk):
    historico = get_object_or_404(HistoricoAtividade, pk=pk, usuario=request.user)
    if request.method == 'POST':
        historico.delete()
        messages.success(request, 'Registro excluído com sucesso!')
        return redirect('historico')
    return render(request, 'core/confirm_delete.html', {'objeto': historico, 'voltar': 'historico'})
