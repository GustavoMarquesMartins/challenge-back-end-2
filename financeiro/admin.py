from django.contrib import admin
from .models import *


class Receitas(admin.ModelAdmin):
    """
    Configuração personalizada para a administração de Receitas.
    """
    # Campos a serem exibidos na listagem
    list_display = ('id', 'descricao', 'data', 'valor')

    # Links para detalhes do objeto na listagem
    list_display_links = ('id',)

    # Campos disponíveis para pesquisa
    search_fields = ('id', 'descricao', 'data', 'valor')

    # Campos editáveis diretamente na listagem
    list_editable = ('valor',)

    # Número de itens por página
    list_per_page = 10

# Registro da classe Receita com as configurações personalizadas
admin.site.register(Receita, Receitas)

class Despesas(admin.ModelAdmin):
    """
    Configuração personalizada para a administração de Despesas.
    """
    # Campos a serem exibidos na listagem
    list_display = ('id', 'descricao', 'data', 'valor')

    # Links para detalhes do objeto na listagem
    list_display_links = ('id',)

    # Campos disponíveis para pesquisa
    search_fields = ('id', 'descricao', 'data', 'valor')

    # Campos editáveis diretamente na listagem
    list_editable = ('valor',)

    # Número de itens por página
    list_per_page = 10

# Registro da classe Receita com as configurações personalizadas
admin.site.register(Despesa, Despesas)

class Resumos(admin.ModelAdmin):
    """
    Configuração personalizada para a administração de Resumos.
    """
    # Campos a serem exibidos na listagem
    list_display = ('id', 'valor_total_receitas', 'valor_total_receitas', 'data')

    # Links para detalhes do objeto na listagem
    list_display_links = ('id',)

    # Campos disponíveis para pesquisa
    search_fields = ('id',)

    # Campos editáveis diretamente na listagem
    list_editable = ('valor_total_receitas', 'valor_total_receitas', 'data')

# Registro da classe Receita com as configurações personalizadas
admin.site.register(Resumo, Resumos)