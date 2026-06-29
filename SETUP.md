# FitRoutine — Como rodar o projeto

## 1. Instalar dependências
No terminal, dentro da pasta do projeto (onde está o `manage.py`):

```
pip install -r requirements.txt
```

## 2. Criar o banco de dados
```
python manage.py migrate
```

## 3. Criar o login de administrador (superusuário)
Esse é o usuário que vai ver o botão **"Painel Admin"** na navbar e acessar `/admin/`.

```
python manage.py createsuperuser
```
Vai pedir um nome de usuário, e-mail (pode deixar em branco) e senha.

## 4. (Opcional) Popular dados iniciais
Cria automaticamente algumas Categorias, Grupos Musculares e Exercícios de exemplo:

```
python manage.py seed_db
```

## 5. Rodar o servidor
```
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

- Cadastre um usuário comum pela tela de "Cadastrar" para testar como usuário normal.
- Faça login com o superusuário criado no passo 3 para ver o botão "Painel Admin" na navbar e acessar o Django Admin em `/admin/`.

## O que foi adicionado/ajustado nesta versão

- CRUD completo (criar, listar, editar, excluir) para todas as 11 funcionalidades:
  Exercícios, Categorias de Exercício, Grupos Musculares, Planejamento Semanal,
  Atividades Diárias, Calendário, Metas Semanais, Anotações, Histórico de
  Atividades, Cadastro/Login de usuário e Painel Administrativo (login admin).
- Navbar fixa (sempre visível durante a navegação) com todos os 11 itens.
- Botão "Painel Admin" que só aparece para usuários com `is_staff=True`, levando para `/admin/`.
- Todas as 9 entidades do banco registradas individualmente no Django Admin
  (além dos inlines), para ficar visível que cada uma tem sua tela própria.
- Inlines no Django Admin:
  - Exercícios dentro de Categoria de Exercício
  - Exercícios dentro de Grupo Muscular
  - Atividades Diárias dentro de Planejamento Semanal
  - Histórico de Atividade dentro de Atividade Diária
