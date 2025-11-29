from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano = models.PositiveIntegerField()
    disponivel = models.BooleanField(default=True)

    def str(self):
        return f"{self.titulo} - {self.autor}"
    

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def str(self):
        return f"{self.livro} emprestado por {self.usuario.email}"


