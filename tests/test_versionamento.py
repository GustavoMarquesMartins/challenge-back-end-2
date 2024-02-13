from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class VersionamentoTestCase(APITestCase):

  fixtures = ['despesas_iniciais']

  def setUp(self):
    """Método executado antes de cada teste"""
    self.lista_url = reverse('despesas-list')
  
  def test_solicitacao_de_versao(self):
    """Verifica se a versao solicitada para a api esta sendo retornada"""
    url_versao = self.lista_url + '?version=2'
    resposta = self.client.get(url_versao)
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    self.assertEqual(resposta.wsgi_request.GET['version'], '2')
      


  

    
