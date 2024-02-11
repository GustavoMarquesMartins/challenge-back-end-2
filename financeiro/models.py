from django.db import models
from datetime import datetime


class Receita(models.Model):
    """
    Modelo para registros de rendas mensais.
    """
    descricao = models.CharField(max_length=50, blank=False, null=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    data = models.DateTimeField(default=datetime.now, null=False, blank=False)

    def __str__(self):
        """Retorna uma representação em string da descrição do objeto"""
        return f'Descrição da receita: {self.descricao}'

class Despesa(models.Model):
    """
    Modelo para registros de gastos ou despesas mensais.
    """
    descricao = models.CharField(max_length=50, blank=False, null=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    data = models.DateTimeField(default=datetime.now, null=False, blank=False)

    def __str__(self):
        """Retorna uma representação em string da descrição do objeto"""
        return f'Descrição da despesa: {self.descricao}'
