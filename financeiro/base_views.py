from rest_framework import viewsets, status, generics
from rest_framework.response import Response
import re
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *


class BaseView():
    """Classe que pode ser usada como base para todas as views"""

    def get_custom_serializer_class(self, lista_serializers):
        """
        Verifica se a versão passada existe. Se existir, retorna o serializador correspondente.
        Caso contrário, retorna o serializador da versão inicial.
        """
        versao_inicial = lista_serializers[0]
        versao = int(self.request.version) if self.request.version else None 
        if versao:
            versao_solicitada_existe = versao in range(1, len(lista_serializers) + 1)
            if not versao_solicitada_existe:
                return versao_inicial
            versao_solicitada = lista_serializers[versao - 1]
            return versao_solicitada
        else:
            return versao_inicial

    def get_list_serializers(self):
        """Retorna a lista de serializadores de acordo com o modelo passado."""
        model =  self.queryset.model
        if model:
            if model == Receita:
                return [ReceitaSerializer]
            if model == Despesa:
                return [DespesaSerializer, DespesaSerializerV2]
            return None

    def get_serializer_class(self):
        """Define a classe do serializador com base na versão especificada."""
        return self.get_custom_serializer_class(lista_serializers = self.get_list_serializers())

class BaseViewSet(BaseView, viewsets.ModelViewSet):
    """Classe base para todas as ViewSets"""

    # Configuração dos filtros
    filter_backends = [DjangoFilterBackend, filters.SearchFilter] # Backends de filtragem
    filterset_fields = ['descricao'] # Campos filtráveis
    search_fields = ['descricao'] # Campos pesquisáveis

    def create(self, request):
        """Quando uma instância é criada no banco de dados, retorna o cabeçalho 'Location'."""
        class_serializer = self.get_serializer_class()
        serializer = class_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            id = str(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location': self.url_location(request.build_absolute_uri()) + f'{id}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def url_location(self, url):
        """Gera a URL para o campo 'Location'."""
        padrao = r'\?'
        resultado = re.search(padrao, url)
        if resultado:
            indice = resultado.start()
            return url[:indice]
        else:
            return url

class BaseListAPIView(BaseView, generics.ListAPIView):
    """Classe base para todas as ListAPIView"""

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
