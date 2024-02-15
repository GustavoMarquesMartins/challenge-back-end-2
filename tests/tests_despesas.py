from rest_framework.test import APITestCase
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
import json
from datetime import datetime, timedelta
import pytz
from django.utils import timezone

from financeiro.models import Despesa
from financeiro.serializers import DespesaSerializer


class DespesaAPITestCase(APITestCase):

  fixtures = ['despesas_iniciais']

  def setUp(self):
    """
    Configuração inicial antes de cada teste.
    """
    self.lista_url = reverse('despesas-list')

  def test_tenta_buscar_lista_de_despesas(self):
      """
      Testa a busca por uma lista de despesas.
      """
      resposta = self.client.get(self.lista_url)
      self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tenta_buscar_despesa(self):
    """
    Testa a busca por uma despesa específica.
    """
    resposta = self.client.get(self.lista_url + '1/')
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tenta_criar_uma_despesa(self):
    """
    Testa a criação de uma nova despesa.
    """
    resposta = self.client.post(self.lista_url, self.data())
    url_da_requisicao = resposta.wsgi_request.build_absolute_uri()

    self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
    self.assertEqual(resposta['location'], url_da_requisicao + str(resposta.data['id']))

  def test_tenta_deletar_uma_despesa(self):
    """
    Testa a exclusão de uma despesa existente.
    """
    resposta = self.client.delete(self.lista_url + '1/')
    self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)

  def test_tenta_atualizar_uma_despesa(self):
    """
    Testa a atualização de uma despesa existente.
    """
    resposta = self.client.put(self.lista_url + '1/', data=self.data())
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def data(self):
    """
    Retorna um dicionário com os dados a serem enviados na requisição POST.
    """
    return {
        'descricao': 'Despesa com menos de 30 dias criada',
        'valor': 13.00
    }

class DespesaTestCase(TestCase):

  fixtures = ['despesas_iniciais']

  def setUp(self):
    """
    Configuração inicial antes de cada teste.
    """
    self.lista_url = reverse('despesas-list')
    self.gerar_instancia()

  def test_faz_uma_requisicao_com_o_parametro_descricao(self):
    """Quando passada uma URL com o parâmetro 'descricao', deve ser retornada apenas a despesas que atenda a esse parâmetro de pesquisa."""
    descricao = 'Descrição para teste'
    resposta = self.client.get(self.lista_url + f'?descricao={descricao}')
    lista_despesas = resposta.json()
    
    for despesa in lista_despesas:
      self.assertEqual(despesa['descricao'], descricao)

  def test_faz_uma_requisicao_com_o_parametro_mes_e_ano(self):
    """Quando são passados os parâmetros mês e ano usando o método GET, deve ser retornada uma lista de despesas"""
    mes = '{:02d}'.format(self.despesa.data.month)
    ano = self.despesa.data.year

    resposta = self.client.get(self.lista_url + f'{mes}/{ano}/')
    lista_despesas = resposta.json()

    for despesa in lista_despesas:
      data = despesa['data']
      self.assertEqual(data[3:5], str(mes))
      self.assertEqual(data[6:10], str(ano))
  
  def gerar_instancia(self):
    """
    Retorna um dicionário com os dados a serem enviados na requisição POST.
    """
    data = timezone.now()
    self.despesa = Despesa.objects.create( 
      descricao='Descrição para teste',
      valor=1000.00,
      data=data
  )
    return self.despesa


