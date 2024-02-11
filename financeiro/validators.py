from datetime import timedelta, datetime
from .models import Receita


def descricao_valida(model, descricao):
  """Verifica se o campo descrição contém duplicidade para receitas com menos de 30 dias cadastradas"""
  objetos = model.objects.filter(descricao=descricao)
  if objetos:
    for objeto in objetos:
      agora = datetime.now()
      intervalo = objeto.data.day - agora.day
      if intervalo < 30:
        return False
  return True