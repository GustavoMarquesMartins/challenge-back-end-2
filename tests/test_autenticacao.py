from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class AutenticacaoAPITestCase(APITestCase):

  def setUp(self):

    self.url_login = reverse('login')

    self.usuario = User.objects.create_user(username='c3po', password='senha123')
    
    self.credenciais_corretas = {
      "username" : "c3po", 
      "password" : "senha123"
    }

  def test_tentando_realizar_o_login_com_credenciais_corretas(self):
    """Tenta realizar o login com credenciais corretas"""
    
    # Realiza uma requisição para a URL de login usando credenciais corretas
    resposta = self.client.post(self.url_login, self.credenciais_corretas)

    # Verifica se está sendo retornado o token JWT como resposta
    self.assertTrue(resposta.data['access'])
    # Verifica se o código HTTP retornado é 200, indicando que o login foi bem-sucedido
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)
    
  def test_tentando_realizar_o_login_com_credenciais_incorretas(self):
    """Tenta realizar o login com credenciais incorretas"""
    # Credenciais incorretas
    data = {
      "username" : "c3poo", 
      "password" : "senha123", 
    }
    # Realiza uma requisição para a URL de login usando credenciais incorretas
    resposta = self.client.post(self.url_login, data)

    # Verifica se o código HTTP retornado é 401, indicando que o login não foi autorizado
    self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)
      
  def test_tentando_realizar_uma_requisicao_utilizando_o_token_retornado_ao_realizar_o_login(self):
    """Tenta realizar uma requisição para o endpoint de receitas utilizando o token retornado pela API ao realizar o login"""
    # URL do recurso receitas
    url_receitas = reverse('receitas-list')

    # Realizando o login
    resposta = self.client.post(self.url_login, self.credenciais_corretas)
    token_jwt = resposta.data.get('access')

    # Realizando a requisição para a URL de receitas com o token JWT retornado
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_jwt}')
    resposta = self.client.get(url_receitas)
    
    # Verifica se o código HTTP retornado é 200, indicando que a requisição foi bem-sucedida
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_tentando_realizar_uma_requisicao_utilizando_token_incorreto(self):
    """Tenta realizar uma requisição para o endpoint de receitas utilizando um token JWT incorreto"""
    # URL do recurso receitas
    url_receitas = reverse('receitas-list')

    # Realizando a requisição com o token JWT incorreto
    self.client.credentials(HTTP_AUTHORIZATION='Bearer token incorreto')
    resposta = self.client.get(url_receitas)

    # Verifica se o código HTTP retornado é 401, indicando que a requisição não foi autorizada
    self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)
