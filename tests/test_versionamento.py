from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .base_test.base_test import TestBaseClass

class VersionamentoTestCase(TestBaseClass, APITestCase):

  def setUp(self):
    """Método executado antes de cada teste"""
    super().setUp()
    self.lista_url = reverse('despesas-list')
  
  def test_solicitacao_de_versao(self):
    """Verifica se a versao solicitada para a api esta sendo retornada"""
    url_versao = self.lista_url + '?version=2'
    
    resposta = self.client.get(url_versao)
    lista_despesas = resposta.json()
    
    for despesa in lista_despesas:
        self.assertTrue(despesa['categoria'])
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertEqual(resposta.wsgi_request.GET['version'], '2')
      


  

    
