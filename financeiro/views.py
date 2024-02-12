from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse 
import re

from .models import *
from .serializers import *

class BaseViewSet(viewsets.ModelViewSet):

  def get_serializer_class(self, serializers, versao):
    """Verifica se a versao passada existe se ela existe e retornada o serializador se nao, e retornado a o serializer mais recente"""
    versao_mais_recente = serializers[-1] 
    if versao:
      versao_solicitade_existe = int(versao) in range(1, len(serializers) + 1)
      if not versao_solicitade_existe:
          return versao_mais_recente
      versao_solicitada = serializers[int(versao) - 1]
      return versao_solicitada
    else:
       return versao_mais_recente

  def custom_create(self, request, serializer_class):
    """Quando e criado uma instancia no banco de dados e retornada o cabecalho location"""
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        id = str(serializer.data['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers= {'Location': self.url_location(request.build_absolute_uri()) + f'{id}'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  def url_location(self, url):
    """Gera a url para o campo location"""
    regex = r'\?'
    resultado = re.search(regex, url)
    indice = resultado.start()
    if resultado:
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
    self.serializer_class = super().get_serializer_class(serializers=self.lista_serializers, versao=self.request.version)
    return self.serializer_class
  
  def create(self, request):
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())

class DespesaViewSet(BaseViewSet):
  """
  ViewSet para o modelo Despesa.
  """
  queryset = Despesa.objects.all()
  lista_serializers = [DespesaSerializer, DespesaSerializerV2]

  def get_serializer_class(self):
      return super().get_serializer_class(serializers=self.lista_serializers, versao=self.request.version)

  def create(self, request):
    return self.custom_create(request=request, serializer_class=self.get_serializer_class())