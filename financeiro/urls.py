from django.urls import path, include
from rest_framework import routers

from .views import *

# Define um roteador para gerenciar URLs da API
router = routers.DefaultRouter()

# Registra o ViewSet da Receita no roteador, definindo o nome base como 'receitas'
router.register('receitas', ReceitaViewSet, basename='receitas')
router.register('despesas', DespesaViewSet, basename='despesas')

# Configura as URLs da aplicação
urlpatterns = [
    # Inclui as URLs geradas pelo roteador
    path('', include(router.urls)),
    path('receitas/<int:mes>/<int:ano>/', ReceitaListView.as_view(), name='receitas_por_ano_mes'),
    path('despesas/<int:mes>/<int:ano>/', DespesaListView.as_view(), name='despesas_por_ano_mes'),
]
