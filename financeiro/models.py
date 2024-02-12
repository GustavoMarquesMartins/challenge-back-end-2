from django.db import models
from django.utils import timezone

class Receita(models.Model):
    """
    Modelo para registros de rendas mensais.
    """
    descricao = models.CharField(max_length=50, blank=False, null=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    data = models.DateTimeField(default=timezone.now, null=False, blank=False)

    def __str__(self):
        """Retorna uma representação em string da descrição do objeto"""
        return f'Descrição da receita: {self.descricao}'

class Despesa(models.Model):
    """
    Modelo para registros de gastos ou despesas mensais.
    """
    CATEGORIAS = ['alimentação','saúde','moradia','transporte','educação','lazer','imprevistos','outras']
    descricao = models.CharField(max_length=50, blank=False, null=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    data = models.DateTimeField(default=timezone.now, null=False, blank=False)
    categoria = models.CharField(default='outras', max_length=20, choices=[(categoria, categoria) for categoria in CATEGORIAS])

    def __str__(self):
        """Retorna uma representação em string da descrição do objeto"""
        return f'Descrição da despesa: {self.descricao}'
