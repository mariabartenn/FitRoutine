from django.db import models
from django.contrib.auth.models import User

class CategoriaExercicio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    icone = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class GrupoMuscular(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Exercicio(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaExercicio, on_delete=models.CASCADE)
    grupo_muscular = models.ForeignKey(GrupoMuscular, on_delete=models.CASCADE)
    duracao_sugerida = models.PositiveIntegerField(blank=True, null=True)
    series_sugeridas = models.PositiveIntegerField(blank=True, null=True)
    repeticoes_sugeridas = models.PositiveIntegerField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class PlanejamentoSemanal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.data_inicio} - {self.data_fim})"

class AtividadeDiaria(models.Model):
    DIAS_DA_SEMANA = [
        ('SEG', 'Segunda-feira'),
        ('TER', 'Terça-feira'),
        ('QUA', 'Quarta-feira'),
        ('QUI', 'Quinta-feira'),
        ('SEX', 'Sexta-feira'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    planejamento = models.ForeignKey(PlanejamentoSemanal, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20, choices=DIAS_DA_SEMANA)
    horario = models.TimeField()
    duracao = models.PositiveIntegerField()
    series = models.PositiveIntegerField(blank=True, null=True)
    repeticoes = models.PositiveIntegerField(blank=True, null=True)
    concluida = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercicio.nome} - {self.dia_semana} {self.horario}"

class MetaSemanal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=300)
    quantidade_treinos = models.PositiveIntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    concluida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

class Anotacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class HistoricoAtividade(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    atividade = models.ForeignKey(AtividadeDiaria, on_delete=models.CASCADE)
    data_realizada = models.DateField()
    duracao_real = models.PositiveIntegerField(blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    registrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Histórico: {self.atividade.exercicio.nome} em {self.data_realizada}"
