from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas gerais
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # 1. Exercícios
    path('exercicios/', views.exercicios_list, name='exercicios'),
    path('exercicios/novo/', views.exercicio_create, name='exercicio_create'),
    path('exercicios/<int:pk>/editar/', views.exercicio_update, name='exercicio_update'),
    path('exercicios/<int:pk>/excluir/', views.exercicio_delete, name='exercicio_delete'),

    # 2. Categorias de Exercício
    path('categorias/', views.categorias_list, name='categorias'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.categoria_delete, name='categoria_delete'),

    # 3. Grupos Musculares
    path('grupos/', views.grupos_list, name='grupos'),
    path('grupos/novo/', views.grupo_create, name='grupo_create'),
    path('grupos/<int:pk>/editar/', views.grupo_update, name='grupo_update'),
    path('grupos/<int:pk>/excluir/', views.grupo_delete, name='grupo_delete'),

    # 4. Planejamento Semanal
    path('planejamento/', views.planejamento_list, name='planejamentos'),
    path('planejamento/novo/', views.planejamento_create, name='planejamento_create'),
    path('planejamento/<int:pk>/', views.planejamento_detail, name='planejamento_detail'),
    path('planejamento/<int:pk>/editar/', views.planejamento_update, name='planejamento_update'),
    path('planejamento/<int:pk>/excluir/', views.planejamento_delete, name='planejamento_delete'),

    # 5. Atividades Diárias
    path('atividade/<int:pk>/editar/', views.atividade_update, name='atividade_update'),
    path('atividade/<int:pk>/excluir/', views.atividade_delete, name='atividade_delete'),
    path('atividade/<int:pk>/concluir/', views.marcar_concluida, name='marcar_concluida'),

    # 6. Calendário
    path('calendario/', views.calendario, name='calendario'),

    # 7. Metas Semanais
    path('metas/', views.metas_list, name='metas'),
    path('metas/nova/', views.meta_create, name='meta_create'),
    path('metas/<int:pk>/editar/', views.meta_update, name='meta_update'),
    path('metas/<int:pk>/excluir/', views.meta_delete, name='meta_delete'),
    path('metas/<int:pk>/concluir/', views.meta_concluir, name='meta_concluir'),

    # 8. Anotações
    path('anotacoes/', views.anotacoes_list, name='anotacoes'),
    path('anotacoes/nova/', views.anotacao_create, name='anotacao_create'),
    path('anotacoes/<int:pk>/editar/', views.anotacao_update, name='anotacao_update'),
    path('anotacoes/<int:pk>/excluir/', views.anotacao_delete, name='anotacao_delete'),

    # 9. Histórico de Atividades
    path('historico/', views.historico_list, name='historico'),
    path('historico/novo/', views.historico_create, name='historico_create'),
    path('historico/<int:pk>/excluir/', views.historico_delete, name='historico_delete'),
]
