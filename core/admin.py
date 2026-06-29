from django.contrib import admin
from .models import (
    CategoriaExercicio, GrupoMuscular, Exercicio,
    PlanejamentoSemanal, AtividadeDiaria, MetaSemanal,
    Anotacao, HistoricoAtividade
)


# ---------------------------------------------------------------------------
# INLINES
# ---------------------------------------------------------------------------

class ExercicioInline(admin.TabularInline):
    """Mostra os Exercícios dentro de Categoria e Grupo Muscular."""
    model = Exercicio
    extra = 1


class AtividadeDiariaInline(admin.TabularInline):
    """Mostra as Atividades Diárias dentro de um Planejamento Semanal."""
    model = AtividadeDiaria
    extra = 1


class HistoricoAtividadeInline(admin.TabularInline):
    """Mostra o Histórico de execução dentro de cada Atividade Diária."""
    model = HistoricoAtividade
    extra = 0


# ---------------------------------------------------------------------------
# 2. CATEGORIA DE EXERCÍCIO
# ---------------------------------------------------------------------------

@admin.register(CategoriaExercicio)
class CategoriaExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)
    inlines = [ExercicioInline]


# ---------------------------------------------------------------------------
# 3. GRUPO MUSCULAR
# ---------------------------------------------------------------------------

@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [ExercicioInline]


# ---------------------------------------------------------------------------
# 1. EXERCÍCIO
# ---------------------------------------------------------------------------

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'grupo_muscular', 'duracao_sugerida', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('categoria', 'grupo_muscular')


# ---------------------------------------------------------------------------
# 4. PLANEJAMENTO SEMANAL
# ---------------------------------------------------------------------------

@admin.register(PlanejamentoSemanal)
class PlanejamentoSemanalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'data_inicio', 'data_fim', 'ativo')
    search_fields = ('nome', 'usuario__username')
    list_filter = ('ativo', 'data_inicio', 'usuario')
    inlines = [AtividadeDiariaInline]


# ---------------------------------------------------------------------------
# 5. ATIVIDADE DIÁRIA (registro próprio, além do inline acima)
# ---------------------------------------------------------------------------

@admin.register(AtividadeDiaria)
class AtividadeDiariaAdmin(admin.ModelAdmin):
    list_display = ('exercicio', 'planejamento', 'dia_semana', 'horario', 'duracao', 'concluida')
    search_fields = ('exercicio__nome', 'planejamento__nome')
    list_filter = ('dia_semana', 'concluida', 'planejamento')
    inlines = [HistoricoAtividadeInline]


# ---------------------------------------------------------------------------
# 7. META SEMANAL
# ---------------------------------------------------------------------------

@admin.register(MetaSemanal)
class MetaSemanalAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'usuario', 'quantidade_treinos', 'data_inicio', 'data_fim', 'concluida')
    search_fields = ('descricao', 'usuario__username')
    list_filter = ('concluida', 'data_inicio', 'usuario')


# ---------------------------------------------------------------------------
# 8. ANOTAÇÃO
# ---------------------------------------------------------------------------

@admin.register(Anotacao)
class AnotacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'data')
    search_fields = ('titulo', 'usuario__username', 'conteudo')
    list_filter = ('data', 'usuario')


# ---------------------------------------------------------------------------
# 9. HISTÓRICO DE ATIVIDADE
# ---------------------------------------------------------------------------

@admin.register(HistoricoAtividade)
class HistoricoAtividadeAdmin(admin.ModelAdmin):
    list_display = ('atividade', 'usuario', 'data_realizada', 'duracao_real')
    search_fields = ('atividade__exercicio__nome', 'usuario__username')
    list_filter = ('data_realizada', 'usuario')
