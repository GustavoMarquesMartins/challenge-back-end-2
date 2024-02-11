from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *

class ReceitaViewSet(viewsets.ModelViewSet):
  """Método que cria os endpoints para o modelo(Receita)"""
  queryset = Receita.objects.all()
  serializer_class = ReceitaSerializer
  
class DespesaViewSet(viewsets.ModelViewSet):
  """Método que cria os endpoints para o modelo(Despesa)"""
  queryset = Despesa.objects.all()
  serializer_class = DespesaSerializer