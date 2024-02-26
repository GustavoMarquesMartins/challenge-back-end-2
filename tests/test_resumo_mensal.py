from django.test import TestCase
from financeiro.models import *
from django.db.models import Sum
from .base_test.base_test import BaseTest
from django.urls import reverse

class ResumoMensalTestCase(BaseTest, TestCase):

  fixtures = ['receitas_iniciais', 'despesas_iniciais']

  def setUp(self):
    """Configura o ambiente antes de cada teste."""
    super().setUp()
    
    self.ano = 2024
    self.mes = 2
    self.lista_url = reverse('resumo_por_ano_mes', args=[self.ano, self.mes])
  
  def test_verifica_valor_retornado_para_valor_total_receitas(self):
    """
    Verifica se o valor total de receitas retornado está correto.

    Verifica se o valor retornado da API para o total de receitas corresponde
    ao valor total de receitas esperado conforme calculado internamente.
    """
    resposta_api = self.client.get(self.lista_url).data['total_receitas']
    self.assertEqual(resposta_api, self.valor_total_receitas())

  def test_verifica_valor_retornado_para_valor_total_despesas(self):
    """
    Verifica se o valor total de despesas retornado está correto.

    Garante que o valor retornado da API para o total de despesas coincide
    com o valor total de despesas esperado, conforme calculado internamente.
    """
    resposta_api = self.client.get(self.lista_url).data['total_despesas']
    self.assertEqual(resposta_api, self.valor_total_despesas())

  def test_verifica_valor_retornado_para_saldo_final(self):
    """
    Verifica se o saldo mensal retornado está correto.

    Certifica-se de que o saldo mensal retornado pela API corresponde
    ao saldo final esperado, conforme calculado internamente.
    """
    resposta_api = self.client.get(self.lista_url).data['saldo_final']
    self.assertEqual(resposta_api, self.saldo_final())

  def test_verifica_valor_retornado_despesas_por_categorias(self):
    """
    Verifica se a despesa por categoria está correta.

    Confirma se os dados das despesas por categoria retornados pela API
    correspondem aos dados esperados das despesas por categoria.
    """
    resposta_api = self.client.get(self.lista_url).data['despesa_por_categoria']
    self.assertEqual(resposta_api, self.despesas_por_categorias())

  def valor_total_receitas(self):
    """Calcula e retorna o valor total das receitas para o mês e ano especificados."""
    return Receita.objects.filter(data__month = self.mes,
                                                  data__year = self.ano) \
                                          .aggregate(total_receitas=Sum('valor'))['total_receitas'] or 0
  
  def valor_total_despesas(self):
    """Calcula e retorna o valor total das despesas para o mês e ano especificados."""
    return Despesa.objects.filter(data__month = self.mes,
                                                  data__year = self.ano) \
                                          .aggregate(total_despesas=Sum('valor'))['total_despesas'] or 0
  
  def saldo_final(self):
    """Calcula e retorna o saldo final do mês."""
    return self.valor_total_receitas() - self.valor_total_despesas()

  def despesas_por_categorias(self):
    """Calcula e retorna os gastos por categoria."""
    return list(Despesa.objects.filter(data__month = self.mes, data__year = self.ano) \
                                                .values('categoria') \
                                                .annotate(valor=Sum('valor')))


    




