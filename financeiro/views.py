from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *

class ReceitaViewSet(viewsets.ModelViewSet):
  """Método que cria os endpoints para o modelo(Receita)"""
  queryset = Receita.objects.all()

  def get_serializer_class(self):
    if self.request.version == 'v2':
      return ReceitaSerializerV2
    else:
      return ReceitaSerializer
  
class DespesaViewSet(viewsets.ModelViewSet):
  """Método que cria os endpoints para o modelo(Despesa)"""
  queryset = Despesa.objects.all()

  def get_serializer_class(self):
    if self.request.version == 'v2':
      return DespesaSerializerV2
    else:
      return ReceitaSerializer
