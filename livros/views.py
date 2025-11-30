from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Livro, Emprestimo
from .serializers import LivroSerializer, EmprestimoSerializer, AlugarLivroSerializer, DevolverLivroSerializer, LivroInputSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers


class LivroListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todos os livros ou busca por título/autor.",
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description="Texto para busca por título ou autor",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: LivroSerializer(many=True)}
    )
    def get(self, request):
        q = request.query_params.get("q", "")

        # Se houver busca, filtrar por título ou autor
        if q:
            livros = Livro.objects.filter(
                titulo__icontains=q
            ) | Livro.objects.filter(
                autor__icontains=q
            )
        else:
            livros = Livro.objects.all()

        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)


class AlugarLivrosView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Aluga um livro específico.",
        request_body=AlugarLivroSerializer,
        responses={201: EmprestimoSerializer(), 400: "Erro"}
    )

    def post(self, request, livro_id):
        try:
            livro = Livro.objects.get(id=livro_id)
        except Livro.DoesNotExist:
            return Response({"erro": "Livro não existe."}, status=404)

        if not livro.disponivel:
            return Response({"erro": "Livro já está emprestado."}, status=400)
        

        emprestimo = Emprestimo.objects.create(
            livro = livro, 
            usuario = request.user
        )

        livro.disponivel = False
        livro.save()
        
        serializer = EmprestimoSerializer(emprestimo)
        return Response(serializer.data, status=201)
    

class ListaEmprestimos(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emprestimos = Emprestimo.objects.filter(usuario=request.user)
        serializer = EmprestimoSerializer(emprestimos, many=True)
        return Response(serializer.data) 


class DevolverLivro(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Devolve um livro previamente alugado.",
        request_body=DevolverLivroSerializer,
        responses={200: "Livro devolvido com sucesso.", 400: "Erro"}
    )

    def post(self, request, emprestimo_id):
        try:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id, usuario=request.user)
        except Emprestimo.DoesNotExist:
            return Response({"erro": "Empréstimo não encontrado."}, status=404)
        
        if emprestimo.data_devolucao:
            return Response({"erro": "Livro já foi devolvido."}, status=400)
        
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()

        emprestimo.livro.disponivel = True
        emprestimo.livro.save()

        return Response({
            "mensagem": "Livro devolvido com sucesso.",
                "data_devolucao": emprestimo.data_devolucao
                }, status=200)


class DeletarLivroView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Deleta um livro pelo ID. Apenas bibliotecários podem deletar.",
        responses={
            200: "Livro excluído com sucesso.",
            403: "Permissão negada.",
            404: "Livro não encontrado."
        }
    )
    
    def delete(self, request, livro_id):
        if not request.user.is_superuser:
            return Response({"detail": "Permissão negada."}, status=403)
        
        try:
            livro = Livro.objects.get(id=livro_id)
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=404)
        
        emprestimo_ativo = Emprestimo.objects.filter(livro=livro, data_devolucao__isnull=True).first()

        if emprestimo_ativo:
            emprestimo_ativo.data_devolucao = timezone.now()
            emprestimo_ativo.save()
        
        livro.delete()

        return Response({"detail": "Livro excluído com sucesso."}, status=200)


class AdicionarLivroView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Adiciona um novo livro. Apenas bibliotecários podem adicionar.",
        request_body=LivroInputSerializer,
        responses={
            201: "Livro criado com sucesso!",
            400: "Erro nos dados fornecidos",
            403: "Permissão negada"
        }
    )

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Apenas bibliotecários podem adicionar livros."},
                status=403
            )
        
        serializer = LivroSerializer(data=request.data)

        if serializer.is_valid():
            livro = serializer.save()
            return Response(
                {
                    "message": "Livro criado com sucesso!",
                    "livro": serializer.data
                },
                status=201
            )
        return Response(serializer.errors, status=400) 


class AtualizaLivroView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Atualiza os dados de um livro pelo ID. Apenas bibliotecários podem atualizar.",
        request_body=LivroInputSerializer,
        responses={
            200: "Livro atualizado com sucesso!",
            400: "Erro nos dados fornecidos",
            403: "Permissão negada",
            404: "Livro não encontrado"
        }
    )

    def post(self, request, livro_id):
        
        if not request.user.is_superuser:
            return Response({"detail": "Apenas bibliotecários podem adicionar editar."}, status=403)
        
        try:
            livro = Livro.objects.get(id=livro_id) 
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=404)
        
        serializer = LivroSerializer(livro, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Livro atualizado com sucesso!", "livro": serializer.data})
        
        return Response(serializer.errors, status=400)

    