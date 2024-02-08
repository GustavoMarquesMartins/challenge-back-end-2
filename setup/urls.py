from django.contrib import admin
from django.urls import path, include

# Define as URLs da aplicação
urlpatterns = [
    # URL para acessar o painel de administração do Django
    path('admin/', admin.site.urls),
    
    # Inclui todas as URLs do app financeiro
    path('', include('financeiro.urls'))
]
