from datetime import timedelta, datetime
from .models import Receita


def descricao_valida(descricao):
  receitas = Receita.objects.filter(descricao=descricao)
  if receitas:
    for receita in receitas:
      agora = datetime.now()
      intervalo = receita.data.day - agora.day
      if intervalo < 30:
        return False
  return True