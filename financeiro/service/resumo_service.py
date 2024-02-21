from financeiro.models import *
from financeiro.serializers import *
from rest_framework.exceptions import ValidationError

import json

class ResumoDoMesService():

  def __init__(self, mes, ano):
    self.ano = ano
    self.mes = mes
    self.set_mes_e_ano()

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
    """Retorna o valor gasto por categoria."""
    despesa_por_categoria = {}

    """
    Verifica para cada despesa se o dicionário 'despesa_por_categoria' possui uma chave com a categoria da descrição.
    Se não existir a categoria, ela é inicializada com o valor  0. Se existir uma chave correspondente, o valor é somado com o valor existente das anteriores.
    """
    for despesa in self.todas_despesas:
      if despesa.categoria not in despesa_por_categoria.keys():
        despesa_por_categoria[despesa.categoria] =  0
      despesa_por_categoria[despesa.categoria] += despesa.valor
      
    return despesa_por_categoria
        
  def set_mes_e_ano(self):

    self.todas_receitas = Receita.objects.filter(
      data__month = self.mes,
      data__year = self.ano
    )

    self.todas_despesas = Despesa.objects.filter(
      data__month = self.mes,
      data__year = self.ano
    )

  def gerar_resumo(self):
    """Verifica se existe um resumo para determinado mês; se sim, ele é retornado. Caso contrário, um é gerado para o mês solicitado."""
    self.resumo = Resumo.objects.filter(
      data__month = self.mes,
      data__year = self.ano
    ).first()

    if not self.resumo:
      """Cria resumo caso não exista um para determinado mês e ano"""
      return self.criar_resumo()
    if self.resumo.saldo_final != self.saldo_final_do_mes():
      """Caso o resumo esteja desatualizado ele e atualizado"""
      return self.atualizar_resumo()
    """Retorna o resumo se não houver necessidade de alterações"""
    return ResumoSerializer(self.resumo)
  
  def criar_resumo(self):
    """Cria uma instância de resumo no banco de dados."""
    resumo = {'valor_total_receitas': self.valor_total_receitas_no_mes(),
              'valor_total_despesas': self.valor_total_despesas_no_mes(),
              'saldo_final': self.saldo_final_do_mes(),
              'valor_gasto_por_categoria': self.saldo_final_do_mes_por_categoria()
              }
    serializer = ResumoSerializer(data=resumo)
    if serializer.is_valid():
      serializer.save()
      return serializer
    raise ValidationError(serializer.erors)
  
  def atualizar_resumo(self):
    """Atualiza uma instância de resumo no banco de dados."""
    data =  {'valor_total_receitas': self.valor_total_receitas_no_mes(),
                'valor_total_despesas': self.valor_total_despesas_no_mes(),
                'saldo_final': self.saldo_final_do_mes(),
                'valor_gasto_por_categoria': self.saldo_final_do_mes_por_categoria()
              }
    serializer = ResumoSerializer(self.resumo, data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return serializer
    raise ValidationError(serializer.erors)
    

    