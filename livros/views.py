from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Livro
from .serializers import LivroSerializer

class LivroListView(APIView):
    permission_classes = [IsAuthenticated]

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
