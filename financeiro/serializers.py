from rest_framework import serializers

from .models import Receita
from .validators import *

class ReceitaSerializer(serializers.ModelSerializer):
    """Serializer para a model Receita"""

    # Utiliza um campo especial para personalizar a representação do valor do campo
    data_formatada = serializers.SerializerMethodField(method_name='get_data_formatada')
    
    class Meta:
        """Configurações do serializer"""
        model = Receita
        fields = ['descricao', 'valor', 'data_formatada']
    
    def get_data_formatada(self, obj):
        """
        Retorna o atributo 'data' formatado como uma string no formato 'dd/mm/aaaa'.
        :param obj: A instância da model Receita.
        """
        return obj.data.strftime('%d/%m/%Y : %H:%M')
    
    def validate(self, data):
        if not descricao_valida(data['descricao']):
            raise serializers.ValidationError({'descricao': 'Uma descrição não pode ter nome duplicado durante 1 mês'})
        return data