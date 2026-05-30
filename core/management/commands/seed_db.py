from django.core.management.base import BaseCommand
from core.models import CategoriaExercicio, GrupoMuscular, Exercicio

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais (Categorias, Grupos Musculares e Exercícios)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Semeando o banco de dados...")

        categorias_data = [
            {'nome': 'Musculação', 'descricao': 'Treino com pesos para hipertrofia e força.', 'icone': 'bi-lightning-charge'},
            {'nome': 'Cardio', 'descricao': 'Atividades cardiovasculares.', 'icone': 'bi-heart-pulse'},
            {'nome': 'Flexibilidade/Mobilidade', 'descricao': 'Alongamentos e posturas.', 'icone': 'bi-person-arms-up'},
            {'nome': 'Funcional', 'descricao': 'Treinos com o peso do corpo ou equipamentos leves.', 'icone': 'bi-activity'}
        ]

        grupos_data = [
            {'nome': 'Peito'}, {'nome': 'Costas'}, {'nome': 'Pernas'}, 
            {'nome': 'Ombros'}, {'nome': 'Braços'}, {'nome': 'Core/Abdômen'},
            {'nome': 'Corpo Todo'}
        ]

        categorias = {}
        for c_data in categorias_data:
            cat, created = CategoriaExercicio.objects.get_or_create(nome=c_data['nome'], defaults=c_data)
            categorias[cat.nome] = cat
            if created:
                self.stdout.write(f"Categoria criada: {cat.nome}")

        grupos = {}
        for g_data in grupos_data:
            grupo, created = GrupoMuscular.objects.get_or_create(nome=g_data['nome'], defaults=g_data)
            grupos[grupo.nome] = grupo
            if created:
                self.stdout.write(f"Grupo Muscular criado: {grupo.nome}")

        exercicios_data = [
            {'nome': 'Supino Reto', 'cat': 'Musculação', 'grupo': 'Peito', 'dur': 45, 'ser': 4, 'rep': 10},
            {'nome': 'Agachamento Livre', 'cat': 'Musculação', 'grupo': 'Pernas', 'dur': 45, 'ser': 4, 'rep': 12},
            {'nome': 'Puxada Frontal', 'cat': 'Musculação', 'grupo': 'Costas', 'dur': 40, 'ser': 3, 'rep': 12},
            {'nome': 'Desenvolvimento com Halteres', 'cat': 'Musculação', 'grupo': 'Ombros', 'dur': 30, 'ser': 3, 'rep': 10},
            {'nome': 'Rosca Direta', 'cat': 'Musculação', 'grupo': 'Braços', 'dur': 30, 'ser': 3, 'rep': 12},
            {'nome': 'Esteira (Corrida Leve)', 'cat': 'Cardio', 'grupo': 'Corpo Todo', 'dur': 30, 'ser': 1, 'rep': 1},
            {'nome': 'Bicicleta Ergométrica', 'cat': 'Cardio', 'grupo': 'Pernas', 'dur': 20, 'ser': 1, 'rep': 1},
            {'nome': 'Prancha Abdominal', 'cat': 'Funcional', 'grupo': 'Core/Abdômen', 'dur': 10, 'ser': 3, 'rep': 1},
            {'nome': 'Burpee', 'cat': 'Funcional', 'grupo': 'Corpo Todo', 'dur': 15, 'ser': 3, 'rep': 15},
            {'nome': 'Alongamento Geral', 'cat': 'Flexibilidade/Mobilidade', 'grupo': 'Corpo Todo', 'dur': 15, 'ser': 1, 'rep': 1},
        ]

        for e_data in exercicios_data:
            Exercicio.objects.get_or_create(
                nome=e_data['nome'],
                defaults={
                    'categoria': categorias[e_data['cat']],
                    'grupo_muscular': grupos[e_data['grupo']],
                    'duracao_sugerida': e_data['dur'],
                    'series_sugeridas': e_data['ser'],
                    'repeticoes_sugeridas': e_data['rep']
                }
            )

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))
