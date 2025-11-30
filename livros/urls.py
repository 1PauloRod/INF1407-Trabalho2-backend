from django.urls import path 
from .views import *

urlpatterns = [
    path("", LivroListView.as_view()),
    path("adicionar/", AdicionarLivroView.as_view()), 
    path("<int:livro_id>/atualizar/", AtualizaLivroView.as_view()), 
    path("<int:livro_id>/deletar/", DeletarLivroView.as_view()),
    path("<int:livro_id>/alugar/", AlugarLivrosView.as_view()), 
    path("meus-emprestimos/", ListaEmprestimos.as_view()),
    path("emprestimo/<int:emprestimo_id>/devolver/", DevolverLivro.as_view())
]


