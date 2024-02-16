from django.test import TestCase

from financeiro.service.resumo_service import ResumoDoMesService
from financeiro.models import *

class ResumoTestCase(TestCase):

  fixtures = ['receitas_iniciais','despesas_iniciais']

  def inicializa_valor_toal_receitas_e_despesas(self, mes, ano):
    self.valor_total_receitas = 0
    self.valor_total_despesas = 0

    self.todas_receitas = Receita.objects.filter(
      data__month = mes,
      data__year = ano
    )

    self.todas_despesas = Despesa.objects.filter(
      data__month = mes,
      data__year = ano
    )
    
    for receita in self.todas_receitas:
      self.valor_total_receitas += receita.valor

    for despesas in self.todas_despesas:
      self.valor_total_despesas += despesas.valor
    
  def setUp(self):
    mes = '02'
    ano = '2024'
    self.resumo = ResumoDoMesService(mes, ano)
    self.inicializa_valor_toal_receitas_e_despesas(mes, ano)

  def test_resumo_valor_total_receitas_mes(self):
    """Deve ser retornado a soma do valor total das receitas no mês"""
    resposta = self.resumo.valor_total_receitas_no_mes()

    self.assertEqual(resposta, self.valor_total_receitas)

  def test_resumo_valor_total_despesas_mes(self):
    """Deve ser retornado a soma do valor total das despesas no mês"""
    resposta = self.resumo.valor_total_despesas_no_mes()

    self.assertEqual(resposta, self.valor_total_despesas)

  def test_resumo_saldo_final_mes(self):
    """Deve retornar o saldo final de um determinado mes e ano"""
    resposta = self.resumo.saldo_final_do_mes()
    resumo_do_mes = self.valor_total_receitas - self.valor_total_despesas 
    self.assertEqual(resumo_do_mes, resposta)
  
  def test_valor_gasto_por_mes_em_cada_categoria(self):
    """Deve retornar o valor gasto por mes em cada categoria"""
    despesa_por_categoria = {}
    for despesa in self.todas_despesas:
      despesa_por_categoria[despesa.categoria] = despesa.valor

    resposta = self.resumo.saldo_final_do_mes_por_categoria()
    
    self.assertEqual(resposta, despesa_por_categoria)
