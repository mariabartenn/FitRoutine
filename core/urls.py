from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('exercicios/', views.exercicios_list, name='exercicios'),
    path('exercicios/novo/', views.exercicio_create, name='exercicio_create'),
    
    path('planejamento/', views.planejamento_list, name='planejamentos'),
    path('planejamento/novo/', views.planejamento_create, name='planejamento_create'),
    path('planejamento/<int:pk>/', views.planejamento_detail, name='planejamento_detail'),
    
    path('calendario/', views.calendario, name='calendario'),
    path('atividade/<int:pk>/concluir/', views.marcar_concluida, name='marcar_concluida'),
    
    path('metas/', views.metas_list, name='metas'),
    path('metas/nova/', views.meta_create, name='meta_create'),
    
    path('historico/', views.historico_list, name='historico'),
    
    path('anotacoes/', views.anotacoes_list, name='anotacoes'),
    path('anotacoes/nova/', views.anotacao_create, name='anotacao_create'),
    
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('grupos/novo/', views.grupo_create, name='grupo_create'),
]
