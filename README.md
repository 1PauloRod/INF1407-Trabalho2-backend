# Biblioteca Online - Sistema de Gerenciamento de Livros

## Descrição do Projeto

Este projeto é um **sistema de biblioteca online**, desenvolvido para permitir que usuários registrem, aluguem e gerenciem livros. O sistema também inclui funcionalidades específicas para **bibliotecários** administrarem os livros do acervo. O objetivo foi criar uma interface intuitiva e responsiva, com foco em usabilidade e organização dos livros alugados.

---

## Funcionalidades Desenvolvidas

### Usuário
- Cadastro de conta com validação de senha (mínimo 8 caracteres, não numérica, não comum).  
- Login e logout.  
- Visualização dos livros alugados, separados entre **pendentes** e **devolvidos**.  
- Possibilidade de devolver livros diretamente pela interface.  
- Pesquisa de livros disponíveis para aluguel.

### Bibliotecário
- Visualização da área administrativa (**home-admin**) com:
  - Listagem de todos os livros.  
  - Pesquisa de livros por título ou autor.  
  - Adição de novos livros.  
  - Edição de informações dos livros.  
  - Exclusão de livros do acervo.  

### Interface
- Layout responsivo, cards organizados, botões claros e mensagens de feedback visíveis.  
- Mensagens de sucesso ou erro no cadastro, atualização ou devolução de livros, sem o uso de `alert()`.  
- Separação clara de livros pendentes e devolvidos na página “Meus Livros”.  

---

## O que Funcionou

- Cadastro e login de usuários.  
- Validação de senha no cadastro.  
- Listagem de livros na área do bibliotecário.  
- Adição, edição e exclusão de livros.  
- Pesquisa de livros.  
- Listagem de livros alugados, com distinção entre pendentes e devolvidos.  
- Devolução de livros pelo usuário com atualização imediata da interface.  
- Feedback de sucesso/erro visível para o usuário.  

---

## O que Não Funcionou

- **Recuperação de senha de usuário**: funcionalidade não implementada.  

---

## Manual do Usuário

### Acesso

1. Abra o navegador e acesse a página de login.  
2. Caso não tenha conta, registre-se no formulário de cadastro, preenchendo nome, sobrenome, email e senha (mínimo 8 caracteres).  

### Área do Usuário

- Ao logar, você será direcionado à página “Home”.  
- Na seção **Meus Livros**:
  - Livros **pendentes** aparecem primeiro.  
  - Livros **devolvidos** aparecem abaixo.  
  - Para devolver um livro, clique no botão **Devolver** ao lado do livro pendente.  
- Pesquise livros disponíveis para aluguel e visualize suas informações básicas.  

### Área do Bibliotecário

- Ao logar como bibliotecário, você acessa a página **Home Admin**.  
- Funcionalidades disponíveis:
  - **Adicionar Livro**: preencha título, autor e ano.  
  - **Editar Livro**: altere informações de livros existentes.  
  - **Excluir Livro**: remova livros do acervo.  
  - **Pesquisar Livro**: encontre livros por título ou autor.  
- Mensagens de sucesso e erro são exibidas abaixo dos formulários, sem o uso de alertas.  

---

## Instruções de Instalação e Uso

### Pré-requisitos

- Python 3.8 ou superior  
- Node.js e npm (para build de TypeScript/JS)  
- Banco de dados: SQLite (padrão) ou PostgreSQL  

### Passos

1. Clone o repositório:
```bash
- git clone <URL_DO_REPOSITORIO>
- cd nome-do-projeto
```

2. Crie e ative um ambiente virtual:
```bash
  python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados e aplique as migrations:
```bash
python manage.py migrate
```

5. (Opcional) Crie um superusuário para testes administrativos:
```bash
python manage.py createsuperuser
```

6. Compile o TypeScript/JS usando npx:
```bash
npx tsc
```

---

## Tecnologias Utilizadas

Frontend: HTML5, CSS3, TypeScript, JavaScript.
Backend: Django, Django REST Framework, Django Token Authentication.
Banco de Dados: SQLite / PostgreSQL.
Outras: LocalStorage para persistência de token, API REST para comunicação frontend-backend.

   
