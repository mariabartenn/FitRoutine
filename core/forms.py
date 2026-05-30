from django import forms
from django.contrib.auth.models import User
from .models import Exercicio, PlanejamentoSemanal, AtividadeDiaria, MetaSemanal, Anotacao, CategoriaExercicio, GrupoMuscular

class CategoriaExercicioForm(forms.ModelForm):
    class Meta:
        model = CategoriaExercicio
        fields = ['nome', 'descricao', 'icone']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
        }

class GrupoMuscularForm(forms.ModelForm):
    class Meta:
        model = GrupoMuscular
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
        }

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = ['nome', 'descricao', 'categoria', 'grupo_muscular', 'duracao_sugerida', 'series_sugeridas', 'repeticoes_sugeridas']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class PlanejamentoSemanalForm(forms.ModelForm):
    class Meta:
        model = PlanejamentoSemanal
        fields = ['nome', 'data_inicio', 'data_fim', 'ativo']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class AtividadeDiariaForm(forms.ModelForm):
    class Meta:
        model = AtividadeDiaria
        fields = ['exercicio', 'dia_semana', 'horario', 'duracao', 'series', 'repeticoes', 'observacoes']
        widgets = {
            'horario': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }

class MetaSemanalForm(forms.ModelForm):
    class Meta:
        model = MetaSemanal
        fields = ['descricao', 'quantidade_treinos', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class AnotacaoForm(forms.ModelForm):
    class Meta:
        model = Anotacao
        fields = ['titulo', 'conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 4}),
        }
