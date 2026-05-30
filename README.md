# FitRoutine

Aplicativo web voltado para auxiliar usuários na organização semanal de exercícios físicos. Uma agenda fitness digital para planejar treinos, registrar frequência e acompanhar metas.

Desenvolvido por: Maria Laura Barten Mariano

## Como rodar o projeto em outra máquina

Siga os passos abaixo para baixar e executar o projeto:

**1. Clone o repositório:**
```bash
git clone https://github.com/mariabartenn/FitRoutine.git
cd FitRoutine
```

**2. Crie e ative o ambiente virtual:**
No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
No Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Prepare o banco de dados:**
```bash
python manage.py migrate
```

**5. (Opcional) Crie um usuário Administrador:**
Para conseguir acessar a área de administração (`/admin`), crie um usuário:
```bash
python manage.py createsuperuser
```

**6. Inicie o servidor local:**
```bash
python manage.py runserver
```

Acesse o aplicativo no navegador através do link: `http://127.0.0.1:8000/`
