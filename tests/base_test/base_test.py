from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

class BaseTest():
  """Classe de teste base para todos os testes relacionados ao recurso de despesas"""
  fixtures = ['despesas_iniciais','receitas_iniciais']

  def setUp(self):
    """Configuração inicial antes de cada teste."""
    
    # Cria um usuário
    self.user = User.objects.create_user(username='c3po', password='123456')

    # Gera um token JWT para o usuário
    self.refresh = RefreshToken.for_user(self.user)
    
    # Força autenticação com o token JWT
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')