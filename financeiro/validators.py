from datetime import timedelta, datetime
from .models import Receita
import pytz

def descricao_valida(model, descricao):
  """Verifica se o campo descrição contém duplicidade para receitas com menos de 30 dias cadastradas"""
  objetos = model.objects.filter(descricao=descricao)
  if objetos:
    for objeto in objetos:
      data_atual = datetime.now(pytz.timezone('America/Sao_Paulo'))
      intervalo = data_atual - objeto.data  
      if intervalo.days < 30:
        return False
  return True