from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configurações do swagger 
schema_view = get_schema_view(
   openapi.Info(
      title="Aluraflix",
      default_version='v1',
      description="Provedor de séries e filmes desenvolvida pela Alura no curso de Django Rest  ",
      terms_of_service="#",
      contact=openapi.Contact(email="c3po@alura.com.br"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # URL para acessar o painel de administração do Django
    path('painel-de-controle-admin/', admin.site.urls),

    # URL para o painel de administração honeypot
    path('admin/', include('admin_honeypot.urls')),
    
    # Inclui todas as URLs do app financeiro
    path('', include('financeiro.urls')),
    
    # Urls de acesso a documentação feita pelo swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
