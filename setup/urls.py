from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # URL para acessar o painel de administração do Django
    path('painel-de-controle-admin/', admin.site.urls),

    # URL para o painel de administração honeypot
    path('admin/', include('admin_honeypot.urls')),
    
    # Inclui todas as URLs do app financeiro
    path('', include('financeiro.urls'))
]
