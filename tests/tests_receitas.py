from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from financeiro.models import Receita
from financeiro.serializers import ReceitaSerializer
import json
from datetime import datetime, timedelta
import pytz


class ReceitaTestCase(APITestCase):

  fixtures = ['receitas_iniciais']

  def setUp(self):
    """
    Configuração inicial antes de cada teste.
    """
    self.lista_url = reverse('receitas-list')

  def test_tenta_buscar_lista_de_receitas(self):
      """
      Testa a busca por uma lista de receitas.
      """
      resposta = self.client.get(self.lista_url)
      self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tenta_buscar_receita(self):
    """
    Testa a busca por uma receita específica.
    """
    resposta = self.client.get(self.lista_url + '1/')
    respota_convertida = self.get_resposta(resposta=resposta)
    
    receita_esperada = Receita.objects.get(pk=1)
    receita_esperada = ReceitaSerializer(instance=receita_esperada)

    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertEqual(respota_convertida, receita_esperada.data)

  def test_tenta_criar_uma_receita(self):
    """
    Testa a criação de uma nova receita.
    """
    resposta = self.client.post(self.lista_url, self.data())
    self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

  def test_tenta_deletar_uma_receita(self):
    """
    Testa a exclusão de uma receita existente.
    """
    resposta = self.client.delete(self.lista_url + '1/')
    self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)

  def test_tenta_atualizar_uma_receita(self):
    """
    Testa a atualização de uma receita existente.
    """
    receita_esperada = Receita.objects.get(pk=1)
    receita_esperada = ReceitaSerializer(instance=receita_esperada)

    resposta = self.client.put(self.lista_url + '1/', data=self.data())
    resposta_convertida = self.get_resposta(resposta=resposta)

    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertNotEqual(resposta_convertida, receita_esperada.data)

  def data(self):
    """
    Retorna um dicionário com os dados a serem enviados na requisição POST.
    """
    return {
        'descricao': 'Receita com menos de 30 dias criada',
        'valor': 13.00
    }

  def get_resposta(self, resposta):
    """
    Converte o objeto retornado pela API em um dicionário Python.
    """
    json_decodificado = resposta.content.decode('UTF-8')
    return json.loads(json_decodificado)