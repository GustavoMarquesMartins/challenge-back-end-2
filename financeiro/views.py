from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .base_views import *

class ReceitaViewSet(BaseViewSet):
  """ViewSet para o modelo Receita"""
  queryset = Receita.objects.all()
  lista_serializers = [ReceitaSerializer]

class DespesaViewSet(BaseViewSet):
  """ViewSet para o modelo Despesa"""
  queryset = Despesa.objects.all()
  lista_serializers = [DespesaSerializer, DespesaSerializerV2]

class ReceitaListView(BaseListAPIView):
  """View para listar receitas com base no mês e ano solicitados"""
  queryset = Receita.objects.all()

class DespesaListView(BaseListAPIView):
  """View para listar despesas com base no mês e ano solicitados"""
  queryset = Despesa.objects.all()

class ResumoListView(APIView):
  """Retorna um resumo mensal"""
  serializers_class = ResumoMensalSerializer
  queryset = Receita.objects.all()
  
  def get(self, *args, **kwargs):
    self.mes = self.kwargs.get('mes')
    self.ano = self.kwargs.get('ano')

    data = {
        'total_receitas': self.total_receitas(),
        'total_despesas': self.total_despesas(),
        'saldo_final': self.saldo_final(),
        'despesa_por_categoria': list(self.despesas_por_categoria())
    }
    return Response(data, status.HTTP_200_OK)
  
  def total_receitas(self):
    """Retorna o valor total de receitas por categoria para o mês e ano especificados"""
    return Receita.objects.filter(data__month = self.mes, 
                                      data__year = self.ano) \
                                .aggregate(total_receitas=Sum('valor'))['total_receitas'] or 0
  def total_despesas(self):
    """Retorna o valor total de despesas para o mês e ano especificados"""
    return Despesa.objects.filter(data__month = self.mes, 
                                            data__year = self.ano) \
                                      .aggregate(total_despesas=Sum('valor'))['total_despesas'] or 0
  def saldo_final(self):
    """Retorna o saldo final para mês e ano especificados"""
    return self.total_receitas() - self.total_despesas()
  
  def despesas_por_categoria(self):
    """Retorna o valor total de despesas por categoria para o mês e ano especificados"""
    return Despesa.objects.filter(data__month = self.mes, 
                                            data__year = self.ano) \
                                              .values('categoria') \
                                              .annotate(valor=Sum('valor'))
     
class Cadastro(CreateAPIView):
  """Cadastra um usuário"""
  serializer_class  = UsuarioSerializer
  permission_classes = [AllowAny]
  
class Login(CreateAPIView):
  """Gera um token de acesso para usuários cadastrados no sistema"""
  serializer_class  = UsuarioSerializer
  permission_classes = [AllowAny]

  def post(self, request):
    username = request.data['username']
    password = request.data['password']

    user = authenticate(username = username, password = password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'},
                         status=status.HTTP_401_UNAUTHORIZED)

    

  
  