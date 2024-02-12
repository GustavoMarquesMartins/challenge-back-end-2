from rest_framework import serializers
from .models import *
from .validators import *

class BaseTransacaoSerializer(serializers.ModelSerializer):
    """Base para ReceitaSerializer e DespesaSerializer."""

    data = serializers.SerializerMethodField(method_name='get_data_formatada')

    def get_data_formatada(self, obj):
        """Retorna 'data' formatada como 'dd/mm/aaaa : HH:MM'."""
        return obj.data.strftime('%d/%m/%Y : %H:%M')

    def validate(self, data):
        """Garante que a descrição não seja duplicada durante 1 mês."""
        if not descricao_valida(self.Meta.model, data['descricao']):
            raise serializers.ValidationError({'descricao': 'Descrição não pode ser duplicada por 1 mês'})
        return data

class ReceitaSerializer(BaseTransacaoSerializer):
    """Serializer para Receita."""

    class Meta:
        """Configurações do serializer."""
        model = Receita
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializer(BaseTransacaoSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data']

class DespesaSerializerV2(BaseTransacaoSerializer):
    """Serializer para Despesa."""

    class Meta:
        """Configurações do serializer."""
        model = Despesa
        fields = ['id','descricao', 'valor', 'data','categoria']
