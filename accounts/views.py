from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Registrar um novo usuário.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "last_name", "email", "password", "password2"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format="email"),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "password2": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={201: "Usuário registrado com sucesso", 400: "Erro de validação"}
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=201)
        return Response(serializer.errors, status=400)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @swagger_auto_schema(
        operation_description="Realiza login e retorna o token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"token": openapi.Schema(type=openapi.TYPE_STRING)}
            ),
            400: "Email não encontrado ou senha incorreta"
        }
    )

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email não encontrado"}, status=400)
        
        user = authenticate(email=user_obj.email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            #login(request, user)
            return Response({"token": token.key})

        return Response({"error": "Senha incorreta"}, status=400)
    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(
        operation_description="Realiza logout do usuário autenticado.",
        responses={200: "Logout realizado com sucesso"}
    )

    def post(self, request):
        request.auth.delete()
        #logout(request)
        return Response({"message": "Logout realizado com sucesso"})
    

def is_bibliotecario(user):
    return user.is_superuser

class UserView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retorna informações do usuário autenticado.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "bibliotecario": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )
        },
    )

    def get(self, request):
        user = request.user
        if is_bibliotecario(user):
            return Response({
                "id": user.id,
                "name": user.first_name, 
                "last_name": user.last_name,
                "email": user.email,
                "bibliotecario": True
            })

        return Response({
                "id": user.id,
                "name": user.first_name, 
                "last_name": user.last_name,
                "email": user.email,
                "bibliotecario": False
            })
    

class AlterarSenhaView(APIView):
    permission_classes = [IsAuthenticated] 

    @swagger_auto_schema(
        operation_description="Altera a senha do usuário autenticado.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["senha_atual", "nova_senha"],
            properties={
                "senha_atual": openapi.Schema(type=openapi.TYPE_STRING),
                "nova_senha": openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: "Senha alterada com sucesso",
            400: "Faltam dados",
            401: "Senha atual incorreta"
        }
    )

    def post(self, request):
        
        senha_atual = request.data.get("senha_atual")
        nova_senha = request.data.get("nova_senha")

        if not senha_atual or not nova_senha:
            return Response({"erro": "Faltam dados"}, status=400)
        
        user = request.user

        if not check_password(senha_atual, request.user.password):
            return Response({"erro": "Senha atual incorreta"}, status=401)
        
        user.set_password(nova_senha) 
        user.save()

        return Response({"status": "Senha alterada com sucesso!"}, status=201)

