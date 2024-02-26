from django.contrib import admin
from .models import Receita, Despesa


class Receitas(admin.ModelAdmin):
    """
    Configuração personalizada para a administração de Receitas.
    """
    list_display = ('id', 'descricao', 'data', 'valor')
    list_display_links = ('id',)
    search_fields = ('id', 'descricao', 'data', 'valor')
    list_editable = ('valor',)
    list_per_page = 10

# Registro da classe Receita com as configurações personalizadas
admin.site.register(Receita, Receitas)


class Despesas(admin.ModelAdmin):
    """
    Configuração personalizada para a administração de Despesas.
    """
    list_display = ('id', 'descricao', 'data', 'valor')
    list_display_links = ('id',)
    search_fields = ('id', 'descricao', 'data', 'valor')
    list_editable = ('valor',)
    list_per_page = 10

# Registro da classe Despesa com as configurações personalizadas
admin.site.register(Despesa, Despesas)
