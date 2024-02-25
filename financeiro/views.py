from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import re
from rest_framework import generics
from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken




from .models import *
from .serializers import *

class BaseView():
  """
  Classe base para todas as views.
  """

  def get_serializer_class(self, serializers, versao):
    """
    Verifica se a versão passada existe. Se ela existir, retorna o serializador correspondente.
    Caso contrário, retorna o serializador da versão inicial.
    """
    versao_inicial = serializers[0]
    if versao:
        versao_solicitada_existe = int(versao) in range(1, len(serializers) +  1)
        if not versao_solicitada_existe:
            return versao_inicial
        versao_solicitada = serializers[int(versao) -  1]
        return versao_solicitada
    else:
        return versao_inicial

  def custom_create(self, request, serializer_class):
    """
    Quando uma instância é criada no banco de dados, retorna o cabeçalho 'location'.
    """
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        id = str(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location': self.url_location(request.build_absolute_uri()) + f'{id}'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def url_location(self, url):
    """
    Gera a URL para o campo 'location'.
    """
    regex = r'\?'
    resultado = re.search(regex, url)
    if resultado:
        indice = resultado.start()
        return url[:indice]
    else:
        return url

  def get_queryset(self):
    """
    Define qual será o queryset usado para realizar a busca no banco de dados.
    Filtra as receitas pela descrição, se um parâmetro de descrição for fornecido.
    """
    parametro = self.request.query_params.get('descricao', None)
    if parametro:
        # Filtra as receitas pela descrição
        self.queryset = self.queryset.model.objects.filter(descricao=parametro)
        return self.queryset
    # Retorna todas as receitas se nenhum parâmetro de descrição for fornecido
    return self.queryset

class ReceitaViewSet(BaseView, viewsets.ModelViewSet):
  """
  ViewSet para o modelo Receita.
  """
  queryset = Receita.objects.all()
  lista_serializers = [ReceitaSerializer]

  def get_serializer_class(self):
    """
    Define a classe do serializador com base na versão da API.
    """
    self.serializer_class = super().get_serializer_class(serializers=get_list_serializers(self.queryset.model),
                                                        versao=self.request.version)
    return self.serializer_class

  def create(self, request):
    """
    Sobrescreve o método create para retornar o status code  201 e o cabeçalho 'location'.
    """
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())

  def get_queryset(self):
    """
    Sobrescreve o método get_queryset para filtrar as receitas com base em parâmetros de consulta.
    """
    return super().get_queryset()

class DespesaViewSet(BaseView, viewsets.ModelViewSet):
  """
  ViewSet para o modelo Despesa.
  """
  queryset = Despesa.objects.all()
  lista_serializers = [DespesaSerializer, DespesaSerializerV2]

  def get_serializer_class(self):
    """
    Define a classe do serializador com base na versão da API.
    """
    self.serializer_class = super().get_serializer_class(serializers=get_list_serializers(self.queryset.model),
                                                        versao=self.request.version)
    return self.serializer_class

  def create(self, request):
    """
    Sobrescreve o método create para retornar o status code   201 e o cabeçalho 'location'.
    """
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())

  def get_queryset(self):
    """
    Sobrescreve o método get_queryset para filtrar as despesas com base em parâmetros de consulta.
    """
    return super().get_queryset()

class ReceitaListView(BaseView, generics.ListAPIView):
  """
  View para listar receitas com base no mês e ano solicitados.
  """
  queryset = Receita.objects.all()

  def get_serializer_class(self):
    """
    Define a classe do serializador com base na versão da API.
    """
    self.serializer_class = super().get_serializer_class(serializers=get_list_serializers(self.queryset.model),
                                                        versao=self.request.version)
    return self.serializer_class

  def get_queryset(self):
    """
    Retorna receitas com base no mês e ano solicitados, caso existam.
    Caso contrário, retorna uma lista vazia.
    """
    ano = self.kwargs.get('ano')
    mes = self.kwargs.get('mes')
    if ano and mes:
        return Receita.objects.filter(
            data__month=mes,
            data__year=ano
        )
    return self.queryset

class DespesaListView(BaseView, generics.ListAPIView):
  """
  View para listar despesas com base no mês e ano solicitados.
  """
  queryset = Despesa.objects.all()

  def get_serializer_class(self):
    """
    Define a classe do serializador com base na versão da API.
    """
    return super().get_serializer_class(serializers=get_list_serializers(self.queryset.model),
                                        versao=self.request.version)
  
  def get_queryset(self):
    """
    Retorna despesas com base no mês e ano solicitados, caso existam.
    Caso contrário, retorna uma lista vazia.
    """
    mes = self.kwargs.get('mes')
    ano = self.kwargs.get('ano')

    if mes and ano:
      return Despesa.objects.filter(
          data__month=mes,
          data__year=ano
        )
    return self.queryset

class ResumoListView(generics.ListAPIView):

  serializers_class = ResumoMensalSerializer
  
  def get(self, request, *args, **kwargs):
    self.mes = self.kwargs.get('mes')
    self.ano = self.kwargs.get('ano')

    data = {
        'total_receitas': self.total_receitas(),
        'total_despesas': self.total_despesas(),
        'saldo_final': self.saldo_final(),
        'despesa_por_categoria': list(self.despesas_por_categoria())
    }
    return Response(data)
  
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
     
def get_list_serializers(model):
   """Retorna a lista de serializers de acordo com o modelo passado"""
   if model:
    if model == Receita:
      return [ReceitaSerializer]
    if model == Despesa:
      return [DespesaSerializer,DespesaSerializerV2]
    return None
    
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

    usuario = authenticate(username = username, password = password)
    if usuario:
      refresh = RefreshToken.for_user(usuario)
      return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciais inválidas'},
                         status=status.HTTP_401_UNAUTHORIZED)

    

  
  