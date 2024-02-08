from rest_framework import serializers
from .models import Receita

class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para a model Receita."""
    data = serializers.ReadOnlyField()
    class Meta:
        """Configurações do serializer."""
        model = Receita
        fields = ['descricao', 'valor', 'data']
