from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

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
    # Retorna receitas do ano e mês especificados
    path('receitas/<int:ano>/<int:mes>/', ReceitaListView.as_view(), name='receitas_por_ano_mes'),
    # Retorna despesas do ano e mês especificados
    path('despesas/<int:ano>/<int:mes>/', DespesaListView.as_view(), name='despesas_por_ano_mes'),
    # Retorna resumo mensal do ano e mês especificados
    path('resumo/<int:ano>/<int:mes>/', ResumoListView.as_view(), name='resumo_por_ano_mes'),
    # Cadastra um usuário para poder realizar login no sistema 
    path('cadastro/', Cadastro.as_view(), name='cadastro'),
    # Realiza login no sistema
    path('login/', Login.as_view(), name='login'),
    # Atualiza o token usando o token refresh
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
