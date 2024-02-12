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
    respota_convertida = self.get_resposta(resposta=resposta)
    
    despesa_esperada = Despesa.objects.get(pk=1)
    despesa_esperada = DespesaSerializer(instance=despesa_esperada)

    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertEqual(respota_convertida, despesa_esperada.data)

  def test_tenta_criar_uma_despesa(self):
    """
    Testa a criação de uma nova despesa.
    """
    resposta = self.client.post(self.lista_url, self.data())
    self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

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
    despesa_esperada = Despesa.objects.get(pk=1)
    despesa_esperada = DespesaSerializer(instance=despesa_esperada)

    resposta = self.client.put(self.lista_url + '1/', data=self.data())
    resposta_convertida = self.get_resposta(resposta=resposta)

    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertNotEqual(resposta_convertida, despesa_esperada.data)

  def data(self):
    """
    Retorna um dicionário com os dados a serem enviados na requisição POST.
    """
    return {
        'descricao': 'Despesa com menos de 30 dias criada',
        'valor': 13.00
    }

  def get_resposta(self, resposta):
    """
    Converte o objeto retornado pela API em um dicionário Python.
    """
    json_decodificado = resposta.content.decode('UTF-8')
    return json.loads(json_decodificado)
