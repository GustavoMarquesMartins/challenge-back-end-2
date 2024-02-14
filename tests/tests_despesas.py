from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from financeiro.models import Despesa
from financeiro.serializers import DespesaSerializer
import json
from datetime import datetime, timedelta
import pytz


class DespesaTestCase(APITestCase):

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
  
  def test_faz_uma_requisicao_com_o_parametro_descricao(self):
    """Quando passada uma URL com o parâmetro 'descricao', deve ser retornada apenas a despesas que atenda a esse parâmetro de pesquisa."""
    descricao = 'Venda de um celular'
    resposta = self.client.get(self.lista_url + f'?descricao={descricao}')
    resposta_dict = resposta.data
    
    for resposta in resposta_dict:
      self.assertEqual(resposta['descricao'], descricao)

  def data(self):
    """
    Retorna um dicionário com os dados a serem enviados na requisição POST.
    """
    return {
        'descricao': 'Despesa com menos de 30 dias criada',
        'valor': 13.00
    }
