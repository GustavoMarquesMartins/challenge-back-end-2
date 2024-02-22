from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import re
from rest_framework import generics
from django.db.models import Sum


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
    mes = self.kwargs.get('mes')
    ano = self.kwargs.get('ano')

    hoje = datetime.today()
    primeiro_dia_do_mes = hoje.replace(day=1)
    proximo_mes = hoje.replace(month=hoje.month + 1)
    ultimo_dia_do_mes = proximo_mes - timedelta(days=1)
    
    total_receitas = Receita.objects.filter(data__range=(primeiro_dia_do_mes, ultimo_dia_do_mes)) \
                                      .aggregate(total_receitas=Sum('valor'))['total_receitas'] or 0

    total_despesas = Despesa.objects.filter(data__range=(primeiro_dia_do_mes, ultimo_dia_do_mes)) \
                                      .aggregate(total_despesas=Sum('valor'))['total_despesas'] or 0

    saldo_final = total_receitas - total_despesas

    despesas_por_categoria = Despesa.objects.filter(data__range=(primeiro_dia_do_mes, ultimo_dia_do_mes)) \
                                              .values('categoria') \
                                              .annotate(total_gasto=Sum('valor'))
    data = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_final': saldo_final,
        'despesas_por_categoria': list(despesas_por_categoria)  # Converte QuerySet para lista
    }

    return Response(data)

def get_list_serializers(model):
   """Retorna a lista de serializers de acordo com o modelo passado"""
   if model:
    if model == Receita:
      return [ReceitaSerializer]
    if model == Despesa:
      return [DespesaSerializer,DespesaSerializerV2]
    return None