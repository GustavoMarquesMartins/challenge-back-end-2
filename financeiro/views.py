from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *

class BaseViewSet(viewsets.ModelViewSet):
  """
  Base ViewSet para modelos.
  """
  def get_serializer_class(self, serializers, versao):
    """
    Retorna o serializer adequado com base na versão especificada.

    Verifica se a versão passada existe dentro da lista de serializers.
    Caso não exista, retorna a versão mais recente.
    Caso exista, retorna a versão solicitada.
    """
    if int(versao) not in range(1, len(serializers) + 1):
        return serializers[-1]
    serializer = serializers[int(versao) - 1]
    return serializer

class ReceitaViewSet(BaseViewSet):
  """
  ViewSet para o modelo Receita.
  """
  queryset = Receita.objects.all()
  lista_serializers = [ReceitaSerializer]

  def get_serializer_class(self):
      return super().get_serializer_class(self.lista_serializers, self.request.version)

class DespesaViewSet(BaseViewSet):
  """
  ViewSet para o modelo Despesa.
  """
  queryset = Despesa.objects.all()
  lista_serializers = [DespesaSerializer, DespesaSerializerV2]

  def get_serializer_class(self):
      return super().get_serializer_class(self.lista_serializers, self.request.version)
