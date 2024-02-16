from financeiro.models import *

class ResumoDoMesService():

  def __init__(self, mes, ano):
    self.set_mes_e_ano(mes=mes, ano=ano)

  def valor_total_receitas_no_mes(self):
    """Retorna o valor todal de receitas de um determinado mes e ano"""
    valor_total_receitas = 0
    
    for receia in self.todas_receitas:
      valor_total_receitas += receia.valor

    return valor_total_receitas
  
  def valor_total_despesas_no_mes(self):
    """Retorna o valor todal de despesas de um determinado mes e ano"""
    valor_total_despesas = 0
    
    for despesa in self.todas_despesas:
      valor_total_despesas += despesa.valor

    return valor_total_despesas

  def saldo_final_do_mes(self):
    """Retorna o saldo final de um determinado mes e ano"""
    valor_total_receitas = self.valor_total_receitas_no_mes()
    valor_total_despesas = self.valor_total_despesas_no_mes()

    return valor_total_receitas - valor_total_despesas

  def saldo_final_do_mes_por_categoria(self):
    """Retorna o valor gasto por categoria """
    despesa_por_categoria = {}
    for despesa in self.todas_despesas:
      despesa_por_categoria[despesa.categoria] = despesa.valor
    return despesa_por_categoria

  def set_mes_e_ano(self, mes, ano):
    self.todas_receitas = Receita.objects.filter(
      data__month = mes,
      data__year = ano
    )

    self.todas_despesas = Despesa.objects.filter(
      data__month = mes,
      data__year = ano
    )
  