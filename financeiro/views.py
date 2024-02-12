from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import re

from .models import *
from .serializers import *

class BaseViewSet(viewsets.ModelViewSet):

  def get_serializer_class(self, serializers, versao):
    """Verifica se a versão passada existe. Se ela existe, é retornado o serializador. Caso contrário, é retornado o serializer de versão inicial"""
    versao_inicial = serializers[-1] 
    if versao:
      versao_solicitade_existe = int(versao) in range(1, len(serializers) + 1)
      if not versao_solicitade_existe:
          return versao_inicial
      versao_solicitada = serializers[int(versao) - 1]
      return versao_solicitada
    else:
       return versao_inicial

  def custom_create(self, request, serializer_class):
    """Quando uma instância é criada no banco de dados, o cabeçalho 'location' é retornado"""
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        id = str(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers= {'Location': self.url_location(request.build_absolute_uri()) + f'{id}'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def url_location(self, url):
    """Gera a URL para o campo location"""
    regex = r'\?'
    resultado = re.search(regex, url)
    if resultado:
      indice = resultado.start()
      return url[:indice] 
    else: 
       return url

class ReceitaViewSet(BaseViewSet):
  """
  ViewSet para o modelo Receita.
  """
  queryset = Receita.objects.all()
  lista_serializers = [ReceitaSerializer]

  def get_serializer_class(self):
    """Define qual a classe serializer"""
    self.serializer_class = super().get_serializer_class(serializers=self.lista_serializers, versao=self.request.version)
    return self.serializer_class
  
  def create(self, request):
    """Sobrescreve o método create para retornar o status code 201 e o campo location"""
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())

class DespesaViewSet(BaseViewSet):
  """
  ViewSet para o modelo Despesa.
  """
  queryset = Despesa.objects.all()
  lista_serializers = [DespesaSerializer, DespesaSerializerV2]

  def get_serializer_class(self):
    """Define qual a classe serializer"""
    return super().get_serializer_class(serializers=self.lista_serializers, versao=self.request.version)

  def create(self, request):
    """Sobrescreve o método create para retornar o status code 201 e o campo location"""
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())