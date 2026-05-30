from django.contrib import admin
from .models import (
    CategoriaExercicio, GrupoMuscular, Exercicio,
    PlanejamentoSemanal, AtividadeDiaria, MetaSemanal,
    Anotacao, HistoricoAtividade
)

class ExercicioInline(admin.TabularInline):
    model = Exercicio
    extra = 1

@admin.register(CategoriaExercicio)
class CategoriaExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)
    inlines = [ExercicioInline]

@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [ExercicioInline]

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'grupo_muscular', 'duracao_sugerida', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('categoria', 'grupo_muscular')

class AtividadeDiariaInline(admin.TabularInline):
    model = AtividadeDiaria
    extra = 1

@admin.register(PlanejamentoSemanal)
class PlanejamentoSemanalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'data_inicio', 'data_fim', 'ativo')
    search_fields = ('nome', 'usuario__username')
    list_filter = ('ativo', 'data_inicio', 'usuario')
    inlines = [AtividadeDiariaInline]

@admin.register(MetaSemanal)
class MetaSemanalAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'usuario', 'quantidade_treinos', 'data_inicio', 'data_fim', 'concluida')
    search_fields = ('descricao', 'usuario__username')
    list_filter = ('concluida', 'data_inicio', 'usuario')

@admin.register(Anotacao)
class AnotacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'data')
    search_fields = ('titulo', 'usuario__username', 'conteudo')
    list_filter = ('data', 'usuario')

@admin.register(HistoricoAtividade)
class HistoricoAtividadeAdmin(admin.ModelAdmin):
    list_display = ('atividade', 'usuario', 'data_realizada', 'duracao_real')
    search_fields = ('atividade__exercicio__nome', 'usuario__username')
    list_filter = ('data_realizada', 'usuario')
