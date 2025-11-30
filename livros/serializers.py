from rest_framework import serializers
from .models import Livro, Emprestimo

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = "__all__"


class AlugarLivroSerializer(serializers.Serializer):
    livro_id = serializers.IntegerField()

class DevolverLivroSerializer(serializers.Serializer):
    emprestimo_id = serializers.IntegerField()

class LivroInputSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    autor = serializers.CharField()
    ano = serializers.IntegerField()
    disponivel = serializers.BooleanField()

    

class EmprestimoSerializer(serializers.ModelSerializer):
    livro = LivroSerializer(read_only=True)

    class Meta:
        model = Emprestimo
        fields = "__all__"