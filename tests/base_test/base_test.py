from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

class TestBaseClass():
  
  fixtures = ['receitas_iniciais', 'despesas_iniciais']
  
  def setUp(self):
    """Configuração inicial antes de cada teste."""
    
    # Cria um usuário
    self.user = User.objects.create_superuser(username='c3po', password='123456')

    # Gera um token JWT para o usuário
    self.refresh = RefreshToken.for_user(self.user)
    
    # Força autenticação com o token JWT
    self.client = APIClient()
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')