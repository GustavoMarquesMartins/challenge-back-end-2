from rest_framework.test import APITestCase
from financeiro.models import Receita
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
import pytz

class ReceitaValidatorsTestCase(APITestCase):
  """Testes para validadores de Receita."""

  def setUp(self):
    """Configura o ambiente antes de cada teste."""
    self.cenario_de_teste()
    self.lista_url = reverse('receitas-list')

  def test_criar_uma_receita_com_a_mesma_descricao_de_uma_receita_criada_a_30_dias_atras(self):
    """Verifica se é possível criar uma nova receita com uma descrição idêntica à de uma receita criada a 30 dias atrás."""
    resposta = self.client.post(self.lista_url, data=self.data_receita_mais_de_30_dias())
    self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

  def test_criar_uma_receita_com_a_mesma_descricao_de_uma_receita_criada_a_menos_de_30_dias_atras(self):
    """Verifica se é possível criar uma nova receita com uma descrição idêntica à de uma receita criada a menos de 30 dias atrás."""
    resposta = self.client.post(self.lista_url, data=self.data_receita_menos_de_30_dias())
    self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

  def test_atualizar_uma_receita_para_uma_mesma_descricao_de_uma_receita_criada_a_mais_de_30_dias_atras(self):
    """Verifica se é possível atualiar uma receita com uma descrição idêntica à de uma receita criada a 30 dias atrás."""
    resposta = self.client.put(self.lista_url + '1/', self.data_receita_mais_de_30_dias())
    self.assertEqual(resposta.status_code, status.HTTP_200_OK)

  def test_atualizar_uma_receita_para_uma_mesma_descricao_de_uma_receita_criada_a_menos_de_30_dias_atras(self):
    """Verifica se é possível atualizar uma receita com uma descrição idêntica à de uma receita criada a menos de 30 dias atrás."""
    resposta = self.client.put(self.lista_url + '1/', data=self.data_receita_menos_de_30_dias())
    self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

  def cenario_de_teste(self): 
    """Cria uma instância de Receita no banco de dados."""
    data_atual = datetime.now()
    data_30_dias_atras = data_atual - timedelta(days=30)
    
    Receita.objects.create(
        descricao='Receita com mais de 30 dias criada',
        data=data_30_dias_atras,
        valor=12.00
    )

    Receita.objects.create(
        descricao='Receita com menos de 30 dias criada',
        data=data_atual,
        valor=12.00
    )

  def data_receita_mais_de_30_dias(self):
    """Retorna um dicionário com os dados serão enviados na requisição POST."""
    return {
        'descricao' : 'Receita com mais de 30 dias criada',
        'valor' : 13.00
    }

  def data_receita_menos_de_30_dias(self):
    """Retorna um dicionário com os dados serão enviados na requisição POST."""
    return {
        'descricao' : 'Receita com menos de 30 dias criada',
        'valor' : 13.00
    }
